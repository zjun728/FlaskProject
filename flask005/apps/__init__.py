import os

from flask import Flask
from apps.utils import create_folder

# print("__init__:", __name__)  # __init__: apps
app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = "who i am? do you know?"

# ./flask003/apps
APPS_DIR = os.path.dirname(__file__)  # os.path.dirname(__file__)为 当前文件__init__.py文件所在路径
# ./flask003/apps/static
STATIC_DIR = os.path.join(APPS_DIR, "static/")
# 数据库文件路径
app.config["DATABASE"] = os.path.join(APPS_DIR, "database.db")
app.config["UPLOADS_RELATIVE"] = "uploads"
# 上传文件存储路径路径
app.config["UPLOADS_FOLDER"] = os.path.join(STATIC_DIR, app.config["UPLOADS_RELATIVE"])
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 限制上传文件大小

create_folder(app.config["UPLOADS_FOLDER"])  # 创建uploads

# app的工作目录
# print("__init__当前目录os：", os.getcwd())
# print("__init__当前目录 __file__：", __file__)
# print("__init__当前目录 os.path.dirname：", os.path.dirname(__file__))

# 防止循环导入报错  app 在导入views之前创建成功（app = Flask(__name__)），
# 才能在views.py模块导入app(from apps import app)时正常导入
import apps.views

# 当前文件作为执行文件（运行）的时候__name__才会等于：__main__
# 当前文件作为包的一个模块导入到文件的时候当前文件的__name__为包名（此为__name__== apps）
# 如：启动runserver.py文件的时候 当前的文件 print( __name__) 输出结果为： apps
# 单独启动__init__.py文件的时候 当前的文件 print( __name__) 输出结果为： __main__
# if __name__ == '__main__':
#     app.run()
