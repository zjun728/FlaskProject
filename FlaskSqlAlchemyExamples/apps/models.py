from flask_sqlalchemy import SQLAlchemy
from apps import app

db = SQLAlchemy(app)


class User(db.Model):  # 创建的数据库表 是类名的小写形式 即表名为；user
    __tablename__ = "user"  # 若果我们不指定数据库表名则创建的数据库表名是类名的小写形式 即表名为；user 若类名为：UserProfile 则表名为：user_profile（大写变小写，中间大写变小写后前面加下划线）
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r, Email %r>' % (self.username, self.email)

# 一对多数据库模型（Person-Address）
# class Person(db.Model):
#     __tablename__ = "person"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     addresses = db.relationship('Address', backref='person', lazy=True)
#
#
# class Address(db.Model):
#     __tablename__ = "address"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), nullable=False)
#     person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
#                           nullable=False)


if __name__ == "__main__":
    # db.create_all()
    # admin = User(username='admin', email='admin@example.com')
    # guest = User(username='guest', email='guest@example.com')
    # peter = User(username='peter', email='peter@example.org')
    #
    # db.session.add(admin)
    # db.session.add(guest)
    # db.session.add(peter)
    # db.session.commit()
    # 查找全部
    # all = User.query.all()  # 查询不需要 commit
    # print(all)
    # 根据名字查找
    # admin_xx = User.query.filter_by(username='admin').first()
    # print(admin_xx)
    # print(admin_xx.email)
    # 根据结尾跟定的字符串查找
    # users = User.query.filter(User.email.endswith("@example.com")).all()
    # 根据开头给定的字符串查找
    # users = User.query.filter(User.email.startswith("@example.com")).all()
    # print(users)
    # 根据用户名排序查找   升序 asc()
    # users = User.query.order_by(User.username.asc()).all()
    # print(users)
    # print("----------------------------")
    # 根据用户名排序查找   降序 desc()
    # users = User.query.order_by(User.username.desc()).all()
    # print(users)

    # 限制用户：
    users = User.query.limit(1).all()
    print(users)
    # 通过主键获取用户：
    users = User.query.get(4)
    print(users)  # 如果没有返回 None
