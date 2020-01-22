import os
from . import mail
from flask_mail import Mail, Message
from flask import Flask, render_template
from . import config

# app = Flask(__name__)


# mail.config['MAIL_SERVER'] = 'smtp.163.com'  # 需要在邮箱里开启smtp服务
# mail.config['MAIL_PORT'] = 465  # 默认端口
# mail.config['MAIL_USE_TLS'] = False  # 启用传输安全层协议  为TRUE时报response错误
# mail.config['MAIL_USE_SSL'] = True  # 启用安全套接层协议
# mail.config['MAIL_USERNAME'] = '18895688852@163.com'  # 正式开发环境不可在脚本中直接显示
# mail.config['MAIL_PASSWORD'] = '798999wan'  # 授权码 正式开发环境不可在脚本中直接显示
# mail.config['FLASK_MAIL_SENDER']='18895688852@163.com'
# mail.config['FLASK_MAIL_SUBJECT_PREFIX'] = '[syt-flask]'
# mail.config['MAIL_DEBUG'] = True

# mail = Mail(app)


msg = Message('title-标题', sender='18895688852@163.com',
              recipients=['823254803@qq.com', '494816251@qq.com', '18895688852@163.com'])
msg.body = 'This is a test of flask-mail.'
msg.html = '<b>test mail<b>'  # 信中显示的是mail.html


# with mail.app_context():
#     mail.send(msg)


# if __name__ == '__main__':
#     app.run()

def send_email(to, subject, template, **kwargs):
    msg = Message(config['development'].FLASKY_MAIL_SUBJECT_PREFIX + subject,
        sender=config['development'].FLASKY_MAIL_SENDER, recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)