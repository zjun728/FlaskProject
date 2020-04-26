from flask import Flask
# pip install mysql-connector
import mysql.connector

app = Flask(__name__)
app.debug = True

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasker.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flasker'
# 配置默认连接到的数据库 flasker 不指定绑定的数据，会自动绑定到默认的数据库（flasker）
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost/flasker'
# 创建数据库模型时（数据库表）指定要绑定的数据库 将当前表创建到指定的数据库中去
app.config['SQLALCHEMY_BINDS'] = {
    'users': 'mysql+mysqlconnector://root:123456@localhost/users',
    'appmeta': 'sqlite:///appmeta.db'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

import apps.views
