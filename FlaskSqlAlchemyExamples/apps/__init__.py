from flask import Flask
# pip install mysql-connector
import mysql.connector
app = Flask(__name__)
app.debug = True

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flasker.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/flasker'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:123456@localhost/flasker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

import apps.views
