from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from flask_login import login_required
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer  as Serializer  # 生成签名令牌，确认账户时使用


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):  # 此方法  返回一个具有可读性的字符串表示模型，可在调试和测试时使用
        return '<Role %r>' % self.name

    users = db.relationship('User', backref='role')  # 反向引用


class User(UserMixin, db.Model):  # UserMixin支持用户登录
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    # 生成确认令牌
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

# db.create_all()

# '''加载用户的回调函数'''
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.route('/secret')
# @login_required
# def secret():
#     return 'Only authenticated users are allowed!'


