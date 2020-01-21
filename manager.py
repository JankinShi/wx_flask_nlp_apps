# 启动脚本,是否也可在启动脚本中注册蓝本？
import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')  # 统一进行实例化
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command('shell', Shell(make_context=make_shell_context()))  # 后可以在命令行中直接使用。
manager.add_command('db', MigrateCommand)  # 后可以在命令行中直接使用。


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    # manager.run(host='0.0.0.0', port='5001')  #使用manager时不允许内部指定端口号 可以python manage.py runserver -p 8066
    manager.run()




