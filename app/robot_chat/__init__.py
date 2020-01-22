# 创建认证蓝本,蓝本构造文件
from flask import Blueprint

robot_chat = Blueprint('robot_chat', __name__)

from . import views