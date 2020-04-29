import shutil
import os
import uuid
from functools import wraps

from flask import session
from flask_uploads import UploadSet, IMAGES, configure_uploads, UploadNotAllowed
from flask import url_for, render_template, request, redirect, flash, make_response
# 密码加密
from werkzeug.security import generate_password_hash
from apps import app, db
from apps.utils import secure_filename_with_uuid, check_filestorages_extension, ALLOWED_IMAGEEXTENSIONS, \
    create_thumbnail, create_show
from apps.forms import RegistForm, LoginForm, PwdForm, InfoForm
from apps.forms import AlbumInfoForm, AlbumUploadForm
from apps.models import User, AlbumTag, Album

# 第二步：产生UploadSet类对象的实例，用来管理上传集合
# Upload Sets 管理上传集合
photosSet = UploadSet(name='photos', extensions=IMAGES)  # 'photos'必须是 app.config['UPLOADED_PHOTOS_DEST']中的 PHOTOS 的小写格式

# 第三步：配置FlaskUpLoad和app,绑定 app 与UploadSet对象实例
configure_uploads(app, photosSet)


# 登录装饰器，检查登录状态
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_name" not in session:
            return redirect(url_for("user_login", next=request.url))  # next表示 当访问某一网页时，如果判断未登陆，则定位到登陆界面
        return f(*args, **kwargs)  # 执行 f 函数本身

    return decorated_function


@app.route('/')
def index():  # 首页
    # print("==================数据库所有用户信息==================")
    # users = query_users_from_db()
    # for user in users:
    #     print(user.tolist())
    # print("=====================================================")

    # print(session)
    # resp = make_response(render_template("index.html"))
    #  resp.set_cookie('qqqq', 'xxxxxxx')
    # return resp
    return render_template("index.html")


# @app.route('/')
# def index():
#     print("首页")
#    return render_template("index.html")

@app.route('/user/login/', methods=['GET', 'POST'])
def user_login():  # 登录

    form = LoginForm()
    if form.validate_on_submit():
        # username = request.form["user_name"]
        username = form.user_name.data
        # userpwd = request.form["user_pwd"]
        userpwd = form.user_pwd.data
        # 查看用户是否存在
        user_one = User.query.filter_by(name=username).first()
        if not user_one:
            # 返回注册界面，重新登录
            flash("用户名不存在！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
            return render_template("user_login.html", form=form)
        else:
            # print(type(userpwd))
            # print(type(user_one.pwd))
            if not user_one.check_pwd(str(userpwd)):
                # 返回注册界面，重新登录
                flash("密码输入错误！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
                return render_template("user_login.html", form=form)
            else:
                # flash("登录成功！", category="ok")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
                session["user_name"] = user_one.name
                session["user_id"] = user_one.id
                # return render_template("index.html") #只返回index.html界面
                return redirect(url_for('index'))  # 重定向界面并执行index路由视图函数

    return render_template("user_login.html", form=form)


@app.route('/user/logout')
@user_login_req
def logout():  # 退出登录
    # remove the username from the session if it's there
    session.pop('user_name', None)
    session.pop("user_id", None)
    return redirect(url_for('index'))


@app.route('/user/regist/', methods=['GET', 'POST'])
def user_regist():  # 注册
    form = RegistForm()
    if form.validate_on_submit():  # 检查提交方式是否为post 验证forms.py定义的validators 验证是否通过
        # 检查用户上传的头像文件名是否符合要求
        # if not check_files_extension([form.user_face.data.filename], ALLOWED_IMAGEEXTENSIONS):
        #     flash("头像文件格式错误！", category="err")
        #     return render_template("user_regist.html", form=form)
        # 查看用户是否存在
        user_name = form.user_name.data
        query_user_by_name = User.query.filter_by(name=user_name).first()
        if query_user_by_name:
            # 返回注册界面，重新注册
            flash("用户名已存在！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
            return render_template("user_regist.html", form=form)

        query_user_by_phone = User.query.filter_by(phone=form.user_phone.data).first()
        if query_user_by_phone:
            # 返回注册界面，重新注册
            flash("手机号已被注册！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
            return render_template("user_regist.html", form=form)
        query_user_by_email = User.query.filter_by(email=form.user_email.data).first()
        if query_user_by_email:
            # 返回注册界面，重新注册
            flash("用户邮箱已被注册注册！", category="err")  # Flashes a message to the next request 闪现一条消息到下一次消息请求
            return render_template("user_regist.html", form=form)

        # print("form", form.user_name.data)
        # print("form", form.data)
        # print("form", form.data["user_name"])
        # print("request.form", request.form)
        user = User()
        # user.name = request.form["user_name"]
        user.name = form.user_name.data
        # user.pwd = request.form["user_pwd"]
        user.pwd = generate_password_hash(form.user_pwd.data)
        # user.age = request.form["user_age"]
        user.phone = form.user_phone.data
        # user.birthday = request.form["user_birthday"]
        user.jianjie = form.user_jianjie.data
        # user.email = request.form["user_email"]
        user.email = form.user_email.data
        # user.face = request.form["user_face"]
        # user.face = form.user_face.data
        # filerstorage = form.user_face.data
        user.uuid = str(uuid.uuid4().hex)[0:10]  # 10个字符长度
        filerstorage = request.files["user_face"]  # 获取头像文件
        user.face = secure_filename_with_uuid(
            filerstorage.filename)  # secure_filename 文件名安全性检测，如果文件名有特殊字符，会将特殊字符转义，没有就返回原文件名
        # print(user.face)

        # 保存用户头像文件
        # user_folder = os.path.join(app.config["UPLOADS_FOLDER"], user.name)
        # create_folder(user_folder)  # 创建用户文件夹
        # filerstorage.save(os.path.join(user_folder, user.face))
        try:
            photosSet.save(storage=filerstorage, folder=user.name, name=user.face)
            # 如果不存在执行插入操作，创建一个用户类 User 的实例
            # 插入一条数据
            db.session.add(user)
            db.session.commit()
            flash("注册成功！", category="ok")
            # username作为查询参数带到url中去
            # 重定向页面 生成url 执行 user_login 函数 跳转到登录界面
            return redirect(url_for("user_login", username=user.name))
        except UploadNotAllowed:
            flash("头像文件格式错误！", category="err")
            return render_template("user_regist.html", form=form)

    return render_template("user_regist.html", form=form)


@app.route('/user/center/', methods=['GET', 'POST'])
@user_login_req
def user_center():  # 个人中心
    return render_template("user_center.html")


@app.route('/user/detail/', methods=['GET', 'POST'])
@user_login_req
def user_detail():  # 个人信息
    user = User.query.get_or_404(int(session.get('user_id')))  # 如果查找不到就抛出404错误
    face_url = photosSet.url(user.name + "/" + user.face)
    print(face_url)
    return render_template("user_detail.html", user=user, face_url=face_url)


@app.route('/user/pwd/', methods=['GET', 'POST'])
@user_login_req
def user_pwd():  # 修改个人密码
    form = PwdForm()
    if form.validate_on_submit():
        old_pwd = request.form["old_pwd"]
        new_pwd = request.form["new_pwd"]
        user = User.query.get_or_404(int(session.get('user_id')))  # 如果查找不到就抛出404错误
        if user.check_pwd(old_pwd):
            user.pwd = generate_password_hash(new_pwd)
            # 更新原数据
            db.session.add(user)  # 当插入数据时，检测到插入的数据主键（id） 已存在 则更新原数据
            db.session.commit()
            session.pop("user_name", None)  # 修改密码后需要重新登录，然后清除session中的数据
            session.pop("user_id", None)
            flash(message="密码修改成功！请重新登录！", category="ok")
            return redirect(url_for("user_login", username=user.name))
        else:
            flash(message="旧密码输入错误！", category="err")
            return render_template("user_pwd.html", form=form)

    return render_template("user_pwd.html", form=form)


@app.route('/user/info/', methods=['GET', 'POST'])
@user_login_req
def user_info():  # 修改个人信息
    user = User.query.get_or_404(int(session.get('user_id')))  # 如果查找不到就抛出404错误

    # 打开修改信息页面，将原来信息展示出来，消息回填

    form = InfoForm()
    if request.method == "GET":
        form.user_jianjie.data = user.jianjie
    if form.validate_on_submit():
        current_login_name = session.get("user_name")

        old_name = user.name
        new_name = request.form["user_name"]
        query_user_by_name = User.query.filter_by(name=new_name).first()
        query_user_by_phone = User.query.filter_by(phone=request.form["user_phone"]).first()
        query_user_by_email = User.query.filter_by(email=request.form["user_email"]).first()
        print()

        if query_user_by_phone != None and user.phone != query_user_by_phone.phone:
            flash(message="手机号已被注册！", category="err")
            print(1111)
            return render_template("user_info.html", user=user, form=form)
        elif query_user_by_email != None and user.email != query_user_by_email.email:
            flash(message="邮箱已被注册！", category="err")
            print(222)
            return render_template("user_info.html", user=user, form=form)
        elif query_user_by_name != None and current_login_name != query_user_by_name.name:  # 如果数据库没有这个用户名或者当前登录的用户名和更改的用户名一样（本人操作），都可以更新个人信息
            flash(message="用户名已存在！", category="err")
            print(333)
            return render_template("user_info.html", user=user, form=form)
        else:
            user.name = request.form["user_name"]
            user.email = request.form["user_email"]
            user.phone = request.form["user_phone"]
            user.jianjie = request.form["user_jianjie"]
            filestorage = request.files["user_face"]  # 获取头像文件
            # filestorage = form.user_face.data  # 获取头像文件
            if filestorage.filename != "":
                # # 检查用户上传的头像文件名是否符合要求
                # if not check_files_extension([form.user_face.data.filename], ALLOWED_IMAGEEXTENSIONS):
                #     flash("头像文件格式错误！", category="err")
                #     return redirect(url_for("user_info"))
                # 若果上传了新的头像文件，首先删除旧的，再保存新的
                # user_folder = os.path.join(app.config["UPLOADS_FOLDER"], old_name)
                # 删除就旧的头像
                # os.remove(path=os.path.join(user_folder, user.face))
                # 获取旧头像的存储路径
                userface_path = photosSet.path(filename=user.face, folder=old_name)
                # 删除就旧的头像
                os.remove(userface_path)

                # 保存新的
                user.face = secure_filename_with_uuid(filestorage.filename)
                # filestorage.save(os.path.join(user_folder, user.face))
                photosSet.save(storage=filestorage, folder=old_name, name=user.face)
                pass
            # 判断是否修改了用户名：如果修改了则同时修改用户上传资源文件夹
            if old_name != new_name:
                os.rename(os.path.join(app.config["UPLOADS_FOLDER"], old_name),
                          os.path.join(app.config["UPLOADS_FOLDER"], new_name))
                pass

            # update_user_by_name(old_name, user)
            db.session.add(user)  # 当插入数据时，检测到插入的数据主键（id） 已存在 则更新原数据
            db.session.commit()
            flash(message="用户信息已更新！", category="ok")
            session["user_name"] = user.name
            session["user_id"] = user.id
            return redirect(url_for("user_detail"))
    return render_template("user_info.html", user=user, form=form)


@app.route('/user/del/', methods=['GET', 'POST'])
@user_login_req
def user_del():  # 注销个人账号
    if request.method == "POST":
        user = User.query.get_or_404(int(session.get('user_id')))  # 如果查找不到就抛出404错误
        current_login_name = session.get("user_name")
        # 删除用户的上传的文件资源
        del_path = os.path.join(app.config["UPLOADS_FOLDER"], current_login_name)
        shutil.rmtree(del_path, ignore_errors=True)  # shutil 文件拷贝、文件删除 的第三方库
        # 删除用户数据库数据
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("logout"))  # 执行退出操作函数
    return render_template("user_del.html")


@app.route('/album/')
def album_index():  # 相册首页
    return render_template("album_index.html")


@app.route('/album/create/', methods=['GET', 'POST'])
@user_login_req
def album_create():  # 相册首页
    form = AlbumInfoForm()
    if form.validate_on_submit():
        album_title = form.album_title.data
        # 判断当前用户是否已经创建该标题的相册   如果相册属于当前用户，且刚创建的相册名称是否已经存在当前登录用户的相册中
        existedCount = Album.query.filter(Album.user_id == session["user_id"], Album.title == album_title).count()
        if existedCount > 0:
            # 相册已经创建过
            flash(message="当前相册已存在，请重新命名相册或更新已有相册！", category="err")
            return render_template("album_create.html", form=form)

        # exsited_count = Album.query.filter_by(title=album_title).count()
        # print(exsited_count)
        # if exsited_count > 0:   # 判断创建的相册标题是否已经存在
        #     flash(message="相册标题已经存在，请重新输入标题！！", category="err")
        #     return render_template("album_create.html", form=form)

        album_desc = form.album_desc.data
        album_privacy = form.album_privacy.data
        album_tag = form.album_tag.data
        album_uuid = str(uuid.uuid4().hex)[0:10]

        exsited = True
        while exsited:  # 确保uuid唯一性
            exsited_count = Album.query.filter_by(uuid=album_uuid).count()
            if exsited_count > 0:  # 判断创建的相册uuid是否已经存在
                print("已存在，重新生成uuid")
                album_uuid = str(uuid.uuid4().hex)[0:10]
            else:
                exsited = False

        album = Album(title=album_title, desc=album_desc, privacy=album_privacy,
                      tag_id=album_tag, uuid=album_uuid, user_id=int(session["user_id"]))

        db.session.add(album)
        db.session.commit()
        return redirect(url_for("album_upload"))
    return render_template("album_create.html", form=form)


@app.route('/album/upload/', methods=['GET', 'POST'])
@user_login_req
def album_upload():  # 相册首页
    form = AlbumUploadForm()
    albums = Album.query.filter_by(user_id=session["user_id"]).all()  # 获取全部相册标签
    # 动态构造form表单数据： 相册的id作为form.album_title.data即 form.album_title.data为当前相册的id
    form.album_title.choices = [(item.id, item.title) for item in albums]  # 获取到数据库中存储的全部相册标签然后动态填写
    if request.method == "POST":
        fses = request.files.getlist("album_upload")  # 获取上传的多个文件
        # 检查文件扩展名，将合格的文件过滤出来
        valid_fses = check_filestorages_extension(fses, allowed_extensions=ALLOWED_IMAGEEXTENSIONS)
        if len(valid_fses) < 1:
            flash(message="只允许上传文件类型：" + str(ALLOWED_IMAGEEXTENSIONS), category="err")
            return redirect(url_for("album_upload"))
        else:
            # 获取当前相册的名称
            files_url = []
            album_title = ""
            for id, title in form.album_title.choices:
                if id == form.album_title.data:
                    album_title = title
            # 开始遍历保存每一个合格文件
            for fs in valid_fses:
                name_origin = secure_filename_with_uuid(fs.filename)
                folder = session.get("user_name") + "/" + album_title
                fname = photosSet.save(fs, folder=folder, name=name_origin)
                ts_path = photosSet.config.destination + "/" + folder
                # 创建并保存缩略图  photosSet.config.destination=app.config['UPLOADED_PHOTOS_DEST']   绝对路径 uploads文件夹
                name_thumb = create_thumbnail(path=ts_path, filename=name_origin, base_width=300)
                # 获取保存缩略图文件的url
                # furl = photosSet.url(fname)  #原图url
                furl = photosSet.url(folder + "/" + name_thumb)
                files_url.append(furl)
                # 创建并保存大图
                name_show = create_show(path=ts_path, filename=name_origin, base_width=800)
                furl = photosSet.url(folder + "/" + name_thumb)
                # files_url.append(furl)

            # 当前上传图片的相册
            print("当前相册id: ", form.album_title.data)
            # 获取当前相册 form构造的时候 相册的id作为form.album_title.data即 form.album_title.data为当前相册的id
            album = Album.query.filter_by(id=form.album_title.data).first()
            album.photonum += len(valid_fses)
            # 更新数据库
            db.session.add(album)
            db.session.commit()
            message = "成功上传 " + str(len(valid_fses)) + " 张图片！！" + "当前相册共有 " + str(album.photonum) + " 张图片！！"
            flash(message=message, category="ok")

            return render_template("album_upload.html", form=form, files_url=files_url)

    return render_template("album_upload.html", form=form)


@app.route('/album/browse/')
def album_browse():  # 相册首页
    return render_template("album_browse.html")


@app.route('/album/list/')
def album_list():  # 相册首页
    return render_template("album_list.html")


# 在该界面一旦请求的url找不到， 触发404错误后，app会找到定义的改路由，返回定义的内容 render_template('page_not_found.html'), 404
@app.errorhandler(404)
def page_not_found(error):
    # return render_template('page_not_found.html'), 404
    resp = make_response(render_template('page_not_found.html'), 404)
    # resp.headers['X-Something'] = 'hahahhaha'
    # resp.set_cookie("aaa","xxxxx")
    return resp
