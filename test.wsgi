import sys

#app's path
sys.path.insert(0,"F:/code/Python_web/flask_blog")

from manager import app

#Initialize WSGI app object
application = app