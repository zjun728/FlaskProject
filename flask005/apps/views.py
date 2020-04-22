import shutil

from werkzeug.utils import secure_filename

from apps import app
from apps.utils import create_folder, secure_filename_with_uuid, check_files_extension, ALLOWED_IMAGEEXTENSIONS

from flask import url_for, render_template, request, redirect, flash, make_response

from apps.forms import RegistForm, LoginForm, PwdForm, InfoForm
from apps.model import User
from flask import session
import sqlite3
import os
from functools import wraps

# 登录装饰器检查登录状态（当未登陆账号时访问个人中心等界面直接跳转到登陆界面）
from apps.sqlite3_manage import query_users_from_db, query_user_by_name, instert_user_to_db, update_user_by_name, \
    delete_user_by_name


def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_name" not in session:
            return redirect(url_for("user_login", next=request.url))  # next表示 当访问某一网页时，如果判断未登陆，则定位到登陆界面
        return f(*args, **kwargs)  # 执行 f 函数本身

    return decorated_function


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

    form = LoginForm()
    if form.validate_on_submit():
        # username = request.form["user_name"]
        username = form.user_name.data
        # userpwd = request.form["user_pwd"]
        userpwd = form.user_pwd.data
        # 查看用户是否存在
        user_one = query_user_by_name(username)
        if not user_one:
            # 返回注册界面，重新登录
            flash("用户名不存在！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
            return render_template("user_login.html", form=form)
        else:
            # print(type(userpwd))
            # print(type(user_one.pwd))
            if str(userpwd) != str(user_one.pwd):
                # 返回注册界面，重新登录
                flash("密码输入错误！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
                return render_template("user_login.html", form=form)
            else:
                # flash("登录成功！", category="ok")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
                session["user_name"] = user_one.name
                # return render_template("index.html") #只返回index.html界面
                return redirect(url_for('index'))  # 重定向界面并执行index路由视图函数

    return render_template("user_login.html", form=form)


@app.route('/logout')
@user_login_req
def logout():  # 退出登录
    # remove the username from the session if it's there
    session.pop('user_name', None)
    return redirect(url_for('index'))


@app.route('/regist/', methods=['GET', 'POST'])
def user_regist():  # 注册
    form = RegistForm()
    if form.validate_on_submit():  # 检查提交方式是否为post 验证forms.py定义的validators 验证是否通过
        # 检查用户上传的头像文件名是否符合要求
        # if not check_files_extension([form.user_face.data.filename], ALLOWED_IMAGEEXTENSIONS):
        #     flash("头像文件格式错误！", category="err")
        #     return render_template("user_regist.html", form=form)
        # 查看用户是否存在
        user_name = form.user_name.data
        user_one = query_user_by_name(user_name)
        if user_one:
            # 返回注册界面，重新注册
            flash("用户名已存在！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求

            return render_template("user_regist.html", form=form)

        # print("form", form.user_name.data)
        # print("form", form.data)
        # print("form", form.data["user_name"])
        # print("request.form", request.form)
        user = User()
        # user.name = request.form["user_name"]
        user.name = form.user_name.data
        # user.pwd = request.form["user_pwd"]
        user.pwd = form.user_pwd.data
        # user.age = request.form["user_age"]
        user.age = form.user_age.data
        # user.birthday = request.form["user_birthday"]
        user.birthday = form.user_birthday.data
        # user.email = request.form["user_email"]
        user.email = form.user_email.data
        # user.face = request.form["user_face"]
        # user.face = form.user_face.data
        # filerstorage = form.user_face.data
        filerstorage = request.files["user_face"]  # 获取头像文件
        user.face = secure_filename_with_uuid(
            filerstorage.filename)  # secure_filename 文件名安全性检测，如果文件名有特殊字符，会将特殊字符转义，没有就返回原文件名
        # print(user.face)

        # 如果不存在执行插入操作
        # 插入一条数据
        instert_user_to_db(user)
        # 保存用户头像文件
        user_folder = os.path.join(app.config["UPLOADS_FOLDER"], user.name)
        create_folder(user_folder)  # 创建用户文件夹
        filerstorage.save(os.path.join(user_folder, user.face))
        flash("注册成功！", category="ok")
        # username作为查询参数带到url中去
        # 重定向页面 生成url 执行 user_login 函数 跳转到登录界面
        return redirect(url_for("user_login", username=user.name))
    return render_template("user_regist.html", form=form)


@app.route('/center/', methods=['GET', 'POST'])
@user_login_req
def user_center():  # 个人中心
    return render_template("user_center.html")


@app.route('/detail/', methods=['GET', 'POST'])
@user_login_req
def user_detail():  # 个人信息
    user = query_user_by_name(session.get("user_name"))
    uploads_folder = app.config["UPLOADS_RELATIVE"]
    return render_template("user_detail.html", uploads_folder=uploads_folder, user=user)


@app.route('/pwd/', methods=['GET', 'POST'])
@user_login_req
def user_pwd():  # 修改个人密码
    form = PwdForm()
    if form.validate_on_submit():
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
            return render_template("user_pwd.html", form=form)

    return render_template("user_pwd.html", form=form)


@app.route('/info/', methods=['GET', 'POST'])
@user_login_req
def user_info():  # 修改个人信息
    user = query_user_by_name(session.get("user_name"))

    # 打开修改信息页面，将原来信息展示出来，消息回填

    form = InfoForm()
    if form.validate_on_submit():

        current_login_name = session.get("user_name")
        old_name = user.name
        new_name = request.form["user_name"]

        query_user = query_user_by_name(new_name)
        if query_user == None or current_login_name == query_user.name:  # 如果数据库没有这个用户名或者当前登录的用户名和更改的用户名一样（本人操作），都可以更新个人信息
            user.name = request.form["user_name"]
            user.email = request.form["user_email"]
            user.age = request.form["user_age"]
            user.birthday = request.form["user_birthday"]
            filestorage = request.files["user_face"]  # 获取头像文件
            #filestorage = form.user_face.data  # 获取头像文件
            if filestorage.filename != "":
                # # 检查用户上传的头像文件名是否符合要求
                # if not check_files_extension([form.user_face.data.filename], ALLOWED_IMAGEEXTENSIONS):
                #     flash("头像文件格式错误！", category="err")
                #     return redirect(url_for("user_info"))
                # 若果上传了新的头像文件，首先删除旧的，再保存新的
                user_folder = os.path.join(app.config["UPLOADS_FOLDER"], old_name)
                # 删除就旧的头像
                os.remove(path=os.path.join(user_folder, user.face))
                # 保存新的
                user.face = secure_filename_with_uuid(filestorage.filename)
                filestorage.save(os.path.join(user_folder, user.face))
                pass
            # 判断是否修改了用户名：如果修改了则同时修改用户上传资源文件夹
            if old_name != new_name:
                os.rename(os.path.join(app.config["UPLOADS_FOLDER"], old_name),
                          os.path.join(app.config["UPLOADS_FOLDER"], new_name))
                pass
            update_user_by_name(old_name, user)
            flash(message="用户信息已更新！", category="ok")
            session.pop("user_name", None)  # 修改密码后需要重新登录，然后清除session中的数据
            session["user_name"] = user.name
            return redirect(url_for("user_detail"))
        else:
            flash(message="用户名已存在！", category="err")

    return render_template("user_info.html", user=user, form=form)


@app.route('/del/', methods=['GET', 'POST'])
@user_login_req
def user_del():  # 注销个人账号
    if request.method == "POST":
        current_login_name = session.get("user_name")
        # 删除用户的上传的文件资源
        del_path = os.path.join(app.config["UPLOADS_FOLDER"], current_login_name)
        shutil.rmtree(del_path, ignore_errors=True)  # shutil文件拷贝，文件删除的第三方库
        # 删除用户数据库数据
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
