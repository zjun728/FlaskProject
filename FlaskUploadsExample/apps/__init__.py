import os

from flask import Flask

from apps.utils import creat_folder

app = Flask(__name__)
app.debug = True

app.config["SECRET_KEY"] = "我有一个小秘密，就不告诉你"

APPS_DiR = os.path.dirname(__file__)  # 得到当前脚本所在的文件路径即：apps文件夹的目录     __file__ ：当前文件路径    即__init__文件所处的文件夹

# print("APPS_DiR",APPS_DiR)
# print("__file__:",__file__)   # __file__: D:\Pyproject\FlaskServer\apps\__init__.py
STATIC_DIR = os.path.join(APPS_DiR, 'static')  # 连接static文件夹目录

app.config['UPLOAD_FOLDER'] = "uploads"  # 相对路径
app.config['ABS_UPLOAD_FOLDER'] = os.path.join(STATIC_DIR, app.config['UPLOAD_FOLDER'])  # 绝对路径
# print(app.config['ABS_UPLOAD_FOLDER'])    # :\Pyproject\FlaskServer\apps\static\uploads


# 第一步：配置上传文件的保存地址
app.config['UPLOADED_PHOTOS_DEST'] = app.config['ABS_UPLOAD_FOLDER']

creat_folder(app.config['ABS_UPLOAD_FOLDER'])

import apps.views  # 只能放到最后，防止循环引用
