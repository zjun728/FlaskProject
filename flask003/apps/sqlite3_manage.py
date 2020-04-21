import os
import sqlite3

from flask import g

from apps import app
from apps.model import User


def connect_db():
    """Connects to the specific database."""
    db = sqlite3.connect(app.config['DATABASE'])
    return db


# 初始化数据库
def init_db():
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql', mode='r') as f:  # mode='r'只读模式 rb可读，可写
            db.cursor().executescript(f.read())  # 执行sql脚本
        db.commit()  # 提交sql表    commit 后断开连接数据库


@app.before_request
def before_request():
    # print('before_request')
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        # print('teardown_request')
        g.db.close()


# 往数据库插入数据
def instert_user_to_db(user):
    # sql_instert = "INSERT INTO users (name, pwd,email,age,birthday,face) VALUES (?, ?, ?, ?, ?, ?)"  # 插入一条语句到users表中

    # 构造  (name, pwd,email,age,birthday,face)
    user_attrs = user.getAttres()
    # 构造  “values (?, ?, ?, ?, ?, ?)"
    values = "VALUES("
    last_attr = user_attrs[-1]
    for attr in user_attrs:
        if attr != last_attr:
            values += "?,"
        else:
            values += "?"
    values += ")"
    sql_instert = "INSERT INTO users" + str(user_attrs) + values  # 插入一条语句到users表中

    # args = [user.name, user.pwd, user.email, user.age, user.birthday, user.face]
    args = user.tolist()
    g.db.execute(sql_instert, args)
    g.db.commit()


# 查询数据库所有数据
def query_users_from_db():
    users = []
    sql_select = "SELECT *FROM users"
    args = []
    cur = g.db.execute(sql_select, args)
    for item in cur.fetchall():
        user = User()
        # item[0] 为id
        # user.name = item[1]
        # user.pwd = item[2]
        # user.email = item[3]
        # user.age = item[4]
        # user.birthday = item[5]
        # user.face = item[6]

        user.fromList(item[1:])  # 第一位为id 从第二位才开始赋值

        users.append(user)
    return users
    pass


# 查询一条数据
def query_user_by_name(user_name):
    sql_select = "SELECT *FROM users WHERE name =?"
    args = [user_name]
    cur = g.db.execute(sql_select, args)
    items = cur.fetchall()  # 取出第一条数据
    if len(items) < 1:
        return None
    first_item = items[0]
    user = User()
    # item[0] 为id
    # user.name = first_item[1]
    # user.pwd = first_item[2]
    # user.email = first_item[3]
    # user.age = first_item[4]
    # user.birthday = first_item[5]
    # user.face = first_item[6]

    user.fromList(first_item[1:])  # 第一位为id 从第二位才开始赋值
    return user


# 清空数据库
def query_user_all():
    dellete_sql = "DELETE FROM users"  # DELETE FROM users 删除全部数据
    args = []
    g.db.execute(dellete_sql)
    g.db.commit()


# 按照条件（name）删除一条数据
def delete_user_by_name(user_name):
    dellete_sql = "DELETE FROM users WHERE name=?"  # DELETE FROM users 删除全部数据
    args = [user_name]
    g.db.execute(dellete_sql, args)
    g.db.commit()


# 更新数据库
def update_user_by_name(old_name, user):
    update_str = ""
    users_attrs = user.getAttres()
    last_attr = users_attrs[-1]
    for attr in users_attrs:
        if attr != last_attr:
            update_str += attr + "=?,"
        else:
            update_str += attr + "=?"
    sql_update = "UPDATE users SET " + update_str + "WHERE name=?"
    args = user.tolist()
    args.append(old_name)
    # print(sql_update)  # UPDATE users SET name=?,pwd=?,email=?,age=?,birthday=?,face=?WHERE name=?
    # print(args)  # ['张小宝', '321', '321@qq', '18', '2020-04-13', '1.jpg', '张大宝']
    g.db.execute(sql_update, args)
    g.db.commit()


# if __name__ == "__main__":
#     print("sqliet3当前目录：", os.getcwd())
#     init_db()
