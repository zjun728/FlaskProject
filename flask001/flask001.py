from flask import Flask, url_for, render_template, request, redirect, g, flash, get_flashed_messages, make_response

from model import User
from flask import session
import sqlite3

from functools import wraps

app = Flask(__name__)
app.config["DATABASE"] = "database.db"
app.config["SECRET_KEY"] = "who i am? do you know?"


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
    print(sql_update)  # UPDATE users SET name=?,pwd=?,email=?,age=?,birthday=?,face=?WHERE name=?
    print(args)  # ['张小宝', '321', '321@qq', '18', '2020-04-13', '1.jpg', '张大宝']
    g.db.execute(sql_update, args)
    g.db.commit()


# 登录装饰器检查登录状态（当未登陆账号时访问个人中心等界面直接跳转到登陆界面）
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_name" not in session:
            return redirect(url_for("user_login", next=request.url))  # next表示 当访问某一网页时，如果判断未登陆，则定位到登陆界面
        return f(*args, **kwargs)  # 执行 f 函数本身

    return decorated_function


# 数据库操作：
# 删除一条数据
# delete_user_by_name("123")
# print("==========================")
# instert_user_to_db(user) #user_regist()
# print("==========================")
# 更新一条数据  修改张大宝信息 张大宝
# user_one = query_user_by_name("张小宝")
# if user_one:
#     user_one.name = "张大宝"
#     user_one.pwd = "321"
#     user_one.age = "18"
#     user_one.email = "321@qq"
#     user_one.birthday = "2020-04-13"
#     update_user_by_name("张小宝", user_one)
# print("==========================")
# 查询所有数据
# users = query_users_from_db()
# for user in users:
#     print(user.tolist())
# print("==========================")

# 查询一条数据
# user_one = query_user_by_name("123")
# if user_one:
#     print(user_one.tolist())
# print("==========================")
#


@app.route('/')
def index():  # 首页
    print("==================数据库所有用户信息==================")
    users = query_users_from_db()
    for user in users:
        print(user.tolist())
    print("=====================================================")

    # print(session)
    # resp = make_response(render_template("index.html"))
    #  resp.set_cookie('qqqq', 'xxxxxxx')
    # return resp
    return render_template("index.html")


# @app.route('/')
# def index():
#     print("首页")
#    return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def user_login():  # 登录
    if request.method == "POST":
        username = request.form["user_name"]
        userpwd = request.form["user_pwd"]
        # 查看用户是否存在
        user_one = query_user_by_name(username)
        if not user_one:
            # 返回注册界面，重新登录
            flash("用户名不存在！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
            return render_template("user_login.html")
        else:
            # print(type(userpwd))
            # print(type(user_one.pwd))
            if str(userpwd) != str(user_one.pwd):
                # 返回注册界面，重新登录
                flash("密码输入错误！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
                return render_template("user_login.html")
            else:
                # flash("登录成功！", category="ok")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
                session["user_name"] = user_one.name
                # return render_template("index.html") #只返回index.html界面
                return redirect(url_for('index'))  # 重定向界面并执行index路由视图函数

    return render_template("user_login.html")


@app.route('/logout')
@user_login_req
def logout():  # 退出登录
    # remove the username from the session if it's there
    session.pop('user_name', None)
    return redirect(url_for('index'))


@app.route('/regist/', methods=['GET', 'POST'])
def user_regist():  # 注册
    if request.method == "POST":
        # print(request.form)
        user = User()
        user.name = request.form["user_name"]
        user.pwd = request.form["user_pwd"]
        user.age = request.form["user_age"]
        user.birthday = request.form["user_birthday"]
        user.email = request.form["user_email"]
        user.face = request.form["user_face"]

        # 查看用户是否存在
        user_one = query_user_by_name(user.name)
        if user_one:
            # 返回注册界面，重新注册
            flash("用户名已存在！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求

            return render_template("user_regist.html")

        # 如果不存在执行插入操作
        # 插入一条数据
        instert_user_to_db(user)
        flash("注册成功！", category="ok")
        # username作为查询参数带到url中去
        ## 重定向页面 生成url 执行 user_login 函数 跳转到登录界面
        return redirect(url_for("user_login", username=user.name))
    return render_template("user_regist.html")


@app.route('/center/', methods=['GET', 'POST'])
@user_login_req
def user_center():  # 个人中心
    return render_template("user_center.html")


@app.route('/detail/', methods=['GET', 'POST'])
@user_login_req
def user_detail():  # 个人信息
    user = query_user_by_name(session.get("user_name"))
    return render_template("user_detail.html", user=user)


@app.route('/pwd/', methods=['GET', 'POST'])
@user_login_req
def user_pwd():  # 修改个人密码
    if request.method == "POST":
        old_pwd = request.form["old_pwd"]
        new_pwd = request.form["new_pwd"]
        user = query_user_by_name(session.get("user_name"))
        if str(old_pwd) == str(user.pwd):
            user.pwd = new_pwd
            update_user_by_name(user.name, user)
            session.pop("user_name", None)  # 修改密码后需要重新登录，然后清除session中的数据
            flash(message="密码修改成功！请重新登录！", category="ok")
            return redirect(url_for("user_login", username=user.name))
        else:
            flash(message="旧密码输入错误！", category="err")
            return render_template("user_pwd.html")

    return render_template("user_pwd.html")


@app.route('/info/', methods=['GET', 'POST'])
@user_login_req
def user_info():  # 修改个人信息
    user = query_user_by_name(session.get("user_name"))

    # 打开修改信息页面，将原来信息展示出来，消息回填

    if request.method == "POST":
        current_login_name = session.get("user_name")
        old_name = user.name
        new_name = request.form["user_name"]

        query_user = query_user_by_name(new_name)
        if query_user == None or current_login_name == query_user.name:  # 如果数据库没有这个用户名或者当前登录的用户名和更改的用户名一样（本人操作），都可以更新个人信息
            user.name = request.form["user_name"]
            user.email = request.form["user_email"]
            user.age = request.form["user_age"]
            user.birthday = request.form["user_birthday"]
            user.face = request.form["user_face"]
            update_user_by_name(old_name, user)
            flash(message="用户信息已更新！", category="ok")
            session.pop("user_name", None)  # 修改密码后需要重新登录，然后清除session中的数据
            session["user_name"] = user.name
            return redirect(url_for("user_detail"))
        else:
            flash(message="用户名已存在！", category="err")

    return render_template("user_info.html", user=user)


@app.route('/del/', methods=['GET', 'POST'])
@user_login_req
def user_del():  # 注销个人账号
    if request.method == "POST":
        current_login_name = session.get("user_name")
        delete_user_by_name(current_login_name)
        return redirect(url_for("logout"))  # 执行退出操作函数
    return render_template("user_del.html")


# 在该界面一旦请求的url找不到， 触发404错误后，app会找到定义的改路由，返回定义的内容 render_template('page_not_found.html'), 404
@app.errorhandler(404)
def page_not_found(error):
    # return render_template('page_not_found.html'), 404
    resp = make_response(render_template('page_not_found.html'), 404)
    # resp.headers['X-Something'] = 'hahahhaha'
    # resp.set_cookie("aaa","xxxxx")
    return resp


if __name__ == '__main__':
    app.run(debug=True)
