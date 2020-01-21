# 创建认证蓝本,蓝本构造文件
from flask import Blueprint

couplets = Blueprint('couplets', __name__)

from . import views  # analysis 或者from ..analysis import  views