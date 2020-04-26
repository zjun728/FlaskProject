from flask_sqlalchemy import SQLAlchemy
from apps import app

db = SQLAlchemy(app)


class User(db.Model):  # 创建的数据库表 是类名的小写形式 即表名为；user
    # 绑定指定的数据库(users) 将当前表创建到指定的数据库中去（__init__.py中定义的数据库）
    __bind_key__ = 'users'
    # __tablename__ = "user"  # 若果我们不指定数据库表名则创建的数据库表名是类名的小写形式 即表名为；user 若类名为：UserProfile 则表名为：user_profile（大写变小写，中间大写变小写后前面加下划线）
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r, Email %r>' % (self.username, self.email)


class AppMeta(db.Model):  # 创建的数据库表 是类名的小写形式 即表名为；user
    # 绑定指定的数据库(appmeta) 将当前表创建到指定的数据库中去（__init__.py中定义的数据库）
    __bind_key__ = 'appmeta'
    # __tablename__ = "user"  # 若果我们不指定数据库表名则创建的数据库表名是类名的小写形式 即表名为；user 若类名为：UserProfile 则表名为：user_profile（大写变小写，中间大写变小写后前面加下划线）
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(80), unique=True, nullable=False)
    appinfo = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r, Email %r>' % (self.username, self.email)


class Person(db.Model):  # 创建的数据库表 是类名的小写形式 即表名为；user
    # 指定绑定的数据库
    # __bind_key__ = 'None' # 不指定绑定的数据，会自动绑定到默认的数据库（flasker）
    # __tablename__ = "user"  # 若果我们不指定数据库表名则创建的数据库表名是类名的小写形式 即表名为；user 若类名为：UserProfile 则表名为：user_profile（大写变小写，中间大写变小写后前面加下划线）
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
    # db.drop_all(bind=None)  # 删除掉默认数据库中的绑定的表（当前应用绑定几个就会删除掉几个） 即flasker中的person（当前就绑定一个表person到flasker数据库中）
    # db.drop_all(bind='users')  # 删除掉users数据库中的表 即users中的user表
    db.drop_all(bind=['users','appmeta'])  # 删除掉users appmeta 数据库中的表 即users（mysql数据库）中的user表 和appmate（sqlite数据库）数据库中的appmate表
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
    # users = User.query.limit(1).all()
    # print(users)
    # # 通过主键获取用户：
    # users = User.query.get(4)
    # print(users)  # 如果没有返回 None
    # 插入数据/更新数据
    # me = User('admin123', 'admin@example.cn')
    # db.session.add(me)    # 当插入数据时，检测到插入的数据主键（id） 已存在 则更新原数据
    # db.session.commit()
    # 删除数据
    # me = User('admin123', 'admin@example.cn')
    # db.session.delete(me)
    # db.session.commit()