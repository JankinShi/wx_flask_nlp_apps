import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    DEBUG = True
    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    # FLASKY_ADMIN ='FLASKY_ADMIN'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True  # 启用安全套接层协议
    MAIL_USERNAME = '18895688852@163.com'  # 正式开发环境不可在脚本中直接显示
    MAIL_PASSWORD = '798999wan'  # 授权码 正式开发环境不可在脚本中直接显示
    FLASKY_MAIL_SENDER='18895688852@163.com'
    FLASKY_MAIL_SUBJECT_PREFIX = '[syt-flask]'
    MAIL_DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:biadmin@123@172.17.1.233/HOSPITAL_CUBEDB_BQL?driver=SQL+Server+Native+Client+10.0"
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:7889@localhost\MSSQLSERVER2012/HOSPITAL_CUBEDB?driver=SQL+Server+Native+Client+10.0"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:7889@localhost/TEST?driver=SQL+Server+Native+Client+10.0"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://sa:7889@localhost/TEST?driver=SQL+Server+Native+Client+10.0"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,

    'default':DevelopmentConfig
}
