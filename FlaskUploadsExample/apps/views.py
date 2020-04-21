import os

from flask import render_template, request, url_for, send_from_directory, flash

from apps import app
# IMAGES 允许上传的扩展名
from flask_uploads import UploadSet, IMAGES, configure_uploads, TEXT, UploadNotAllowed

# 第二步：产生UploadSet类对象的实例，用来管理上传集合
# Upload Sets 管理上传集合
photosSet = UploadSet('photos', IMAGES)  # 'photos'必须是 app.config['UPLOADED_PHOTOS_DEST']中的 PHOTOS 的小写格式
# 第三步：绑定 app 与UploadSet对象实例
configure_uploads(app, photosSet)


@app.route('/index', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        fs = request.files["image_upload"]
        #  print(fs.filename)
        if fs.filename != "":
            # 服务器资源地址
            # file_path = os.path.join(app.config["ABS_UPLOAD_FOLDER"], fs.filename)
            #  print(file_path)
            # fs.save(file_path)    # 这个保存使用了FileStorage 的使用方法保存文件

            # 第四步：使用UploadSet 的save方法保存文件
            # (self, storage, folder=None, name=None):
            # 保存到uploads的根目录   返回的是当前文件的名字  the file will be saved and its name (including the folder) will be returned.
            fname = photosSet.save(fs)  # photosSet.save保存的 文件名fname 会做安全性检查，过滤掉特殊字符 fname可能不是原来的fs.filename 这个文件名了
            print("文件名字：", fname)

            # 浏览器访问的资源地址
            # 原生方法，获取url    url_for
            # file_url = url_for("static",filename="uploads/" + fs.filename)  # static文件夹下的 uploads 文件夹下的 文件名为fs.filename 的文件
            file_url = url_for("static", filename="uploads/" + fname)
            # file_url2 = url_for("uploaded_file",fs.filename)
            file_url2 = url_for("uploaded_file", filename=fname)   # 通过uploaded_file 路由视图函数获取url

            # 第五步：使用UploadSet 的url方法获得文件的url
            file_url3 = photosSet.url(fname)
            print("第一种方式", file_url)
            print("第二种方式", file_url2)
            print("第三种方式", file_url3)
            return render_template('index.html', msg="上传成功", file_url=file_url, file_url2=file_url2,
                                   file_url3=file_url3)

    return render_template('index.html')


@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["ABS_UPLOAD_FOLDER"], filename)


# @app.route('/uploaded/<filename>')
# def uploaded_file(filename):
#     img_path = os.path.join(app.config["ABS_UPLOAD_FOLDER"], filename)
#     print(img_path)
#     if os.path.exists(img_path) == True:
#         print("true")
#         return send_from_directory(app.config["ABS_UPLOAD_FOLDER"], filename)
#     else:
#         print("false")
#         return send_from_directory(app.config["ABS_UPLOAD_FOLDER"], "default.png")


@app.route('/', methods=["GET", "POST"])
def index2():
    if request.method == "POST":
        folder = request.form['image_folder']
        fs = request.files['image_file']
        print(fs.filename != "")
        if fs.filename != "":
            try:
                # fname = photosSet.save(storage=fs, folder=folder)   # photosSet.save会做安全性检查，过滤掉特殊字符 fname可能不是原来的fs.filename
                # fname = photosSet.save(storage=fs, name=folder + "/" + fs.filename)  # 这样不会更改原文件名字
                fname = photosSet.save(storage=fs, folder=folder, name=fs.filename)  # 强制使用原文件名 会保留原文件名字
                print(fname)
            except UploadNotAllowed:
                flash(message="上传文件的类型不被允许！", category='err')
                return render_template('index2.html')
            else:
                # fpath=photosSet.path(filename=fname)
                # fpath = photosSet.path(filename='3.jpg', folder=folder)

                # os.remove(fpath)
                furl = photosSet.url(fname)
                flash(message="上传文件成功！", category='ok')
                return render_template('index2.html', file_url=furl)
    return render_template('index2.html')
