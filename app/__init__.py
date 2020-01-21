#程序工厂函数，create_app() 就是程序的工厂函数，统一实例化，参数就是配置类的名字，即 config.py
# #蓝本一般在实例化的时候注册，在manager.py启动文件中注册也可
from flask import Flask, render_template
from flask_moment import Moment
from config import config
from flask_login import LoginManager
from flask_cors import CORS  # cross origin requests
from flask_restful import Api, Resource


moment = Moment()
api = Api()

'''初始化flask_login'''
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.jinja_env.filters['zip'] = zip  # 添加这个方法

    # CORS(app, resources={r"/getMsg": {"origins": "*"}})
    # CORS(app, supports_credentials=True)  # 让flask支持跨域请求
    CORS(app, resources=r'/*')


    moment.init_app(app)
    login_manager.init_app(app)
    api.init_app(app)

    # 附加路由和自定义错误界面

    # from .main import main as main_buleprint  # 这是注册蓝本
    # app.register_blueprint(main_buleprint)

    # from .auth import auth as auth_blueprint  # 附加认证蓝本
    # app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #
    # from .api_1_0 import api as api_1_0_blueprint  # 注册api蓝本
    # app.register_blueprint(api_1_0_blueprint)

    # from .echarts import echarts as echarts_blueprint  # 注册echarts蓝本
    # app.register_blueprint(echarts_blueprint, url_prefix='/echarts')

    # from .analysis import analysis as analysis_blueprint
    # app.register_blueprint(analysis_blueprint, url_prefix='/analysis')

    # from .couplets import couplets as couplets_blueprint
    # app.register_blueprint(couplets_blueprint)

    from .robot_chat import robot_chat as robot_chat_blueprint
    app.register_blueprint(robot_chat_blueprint)

    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        return response

    app.after_request(after_request)

    app.app_context().push()  # 必须要有上下文
    # db.create_all()  # 必须在程序工厂中创建表
    return app

