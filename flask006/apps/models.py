import uuid as uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from apps import db


class User(db.Model):
    __tablename__ = "user"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    pwd = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    face = db.Column(db.String(255), unique=True, nullable=False)
    jianjie = db.Column(db.TEXT)
    uuid = db.Column(db.String(255), unique=True, nullable=False)
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)
    # addtime = db.Column(db.DATETIME, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % (self.name)

    def check_pwd(self, pwd):
        return self.pwd == pwd


if __name__ == '__main__':
    # 当我们在数据库中写入新的类(表)或者某一表中添加或删除某一属性后需要更新数据库时，
    # 需要将__init__.py脚本中import apps.views 包注释掉，防止循环引用
    db.drop_all(bind=None)
    db.create_all()

