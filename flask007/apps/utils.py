import os
import uuid
from datetime import datetime

from werkzeug.utils import secure_filename


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        os.chmod(folder_path, os.O_RDWR)  # 修改 创建的 文件夹权限 可读可写


# 修改又件名称 原文件名不保存
def change_filename_with_timestamp_uuid(filename):
    fileinfo = os.path.splitext(filename)
    # datetime.now().strftime("%Y%m%d%H%M%S") 时间戳
    # str(uuid.uuid4().hex) uuid
    # fileinfo[-1] 文件后缀名
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1].lower()
    return filename


# 确保文件名安全性并添加时间戳
def secure_filename_with_timestamp(filename):
    fileinfo = os.path.splitext(filename)  # 分割文件名和文件后缀
    filename_prefix = secure_filename(fileinfo[0]) + "_"  # 全中文文件时secure_filename会只保留文件后缀，不包含"."  ,会导致文件重命名出错
    filename = filename_prefix + datetime.now().strftime(" %Y%m%d%H%M%S") + fileinfo[-1].lower()
    return filename


# 确保文件名安全性并添加随机uuid
def secure_filename_with_uuid(filename):
    fileinfo = os.path.splitext(filename)
    filename_prefix = secure_filename(fileinfo[0]) + "_"

    filename = filename_prefix + str(uuid.uuid4().hex)[0:6] + fileinfo[-1].lower()
    return filename


ALLOWED_IMAGEEXTENSIONS = set(["png", "jpg", "jpeg"])
ALLOWED_VIDEO_EXTENSIONS = set(["mp4", "avi"])
ALLOWED_AUDIO_EXTENSIONS = set(["mp3", "m4a"])


# 检查上传控件上传的(多个文件的后缀名是否符合指定的要求
def check_files_extension(filenameslist, allowed_extensions):
    for fname in filenameslist:
        check_state = "." in fname and fname.rsplit(".", 1)[1].lower() in allowed_extensions
    # 只要发现一个文件不合格立即返回False,不去检查剩下的文件
    if not check_state:
        return False
    return True


# 检查上传控件上传的(多个文件的后缀名是否符合指定的要求
def check_filestorages_extension(filestoragelist, allowed_extensions):
    ext_valid_fs = []  # 正确文件的列表
    for fs in filestoragelist:
        #  rsplit() 方法从右侧开始将字符串拆分为列表。 rsplit(".", 1) 从右往左分割，分割一次
        check_state = "." in fs.filename and \
                      fs.filename.rsplit(".", 1)[1].lower() in allowed_extensions
        # 将符合文件加入到列表，返回出去
        if check_state:
            ext_valid_fs.append(fs)
    return ext_valid_fs


# pip3 install pillow
import PIL
from PIL import Image


# 创建缩略图
def create_thumbnail(path, filename, base_width=300):
    imgname, ext = os.path.splitext(filename)
    newfilename = imgname + "_thumb_" + ext  # 缩略图的文件名
    img = Image.open(os.path.join(path, filename))  # 根据指定的路径打开图像文件
    if img.size[0] > base_width:
        # 如果图片宽度小于base_with,不做处理，直接保存
        # 如果图片宽度大于base_width 将其缩放到basewith,并保持图像原来的宽高比
        w_perecent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_perecent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)  # PIL.Image.ANTIALIAS 防锯齿
    img.save(os.path.join(path, newfilename))
    return newfilename


# 创建大图
def create_show(path, filename, base_width=800):
    imgname, ext = os.path.splitext(filename)
    newfilename = imgname + "_show_" + ext  # 展示图的文件名
    img = Image.open(os.path.join(path, filename))  # 根据指定的路径打开图像文件
    if img.size[0] < base_width:
        # 如果图片宽度大于于base_with,不做处理，直接保存
        # 如果图片宽度小于base_width 将其缩放到basewith,并保持图像原来的宽高比
        w_perecent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_perecent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)  # PIL.Image.ANTIALIAS 防锯齿
    img.save(os.path.join(path, newfilename))
    return newfilename
