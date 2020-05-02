import uuid as uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from apps import db
# 密码解密
from werkzeug.security import check_password_hash


# 用户类
class User(db.Model):
    __tablename__ = "user"
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)  # 用户名
    pwd = db.Column(db.String(255), nullable=False)  # 用户密码
    email = db.Column(db.String(120), unique=True, nullable=False)  # 用户邮箱
    phone = db.Column(db.String(120), unique=True, nullable=False)  # 用户手机
    face = db.Column(db.String(255), unique=True, nullable=False)  # 用户头像
    jianjie = db.Column(db.TEXT)  # 用户简介
    uuid = db.Column(db.String(255), unique=True, nullable=False)  # uuid
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 添加时间
    albums = db.relationship("Album", backref="user")  # 定义用户与相册关系
    favors = db.relationship("AlbumFavor", backref="user")  # 定义用户与用户收藏相册关系

    # addtime = db.Column(db.DATETIME, default=datetime.now)

    def __repr__(self):
        return '<User %r>' % (self.name)

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)  # 传入的pwd与解密后的self.pwd相等返回true否则返回false


# 相册标签
class AlbumTag(db.Model):
    __tablename__ = "album_tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)  # 标签名
    albums = db.relationship("Album", backref="album_tag")  # 定义标签与相册关系

    def __repr__(self):
        return '<AlbumTag %r>' % (self.name)


# 相册
class Album(db.Model):
    __tablename__ = "album"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)  # 标题
    desc = db.Column(db.TEXT)  # 描述
    cover = db.Column(db.String(255),default="")  # 相册封面
    photonum = db.Column(db.Integer, default=0)  # 相册图片数量
    privacy = db.Column(db.String(20), default="public")  # 是否私有private私有 protect_1粉丝好友可见 protect_2收藏者可见 public公开
    clicknum = db.Column(db.Integer, default=0)  # 相册浏览量
    favornum = db.Column(db.Integer, default=0)  # 相册收藏量
    uuid = db.Column(db.String(255), unique=True, nullable=False)  # uuid
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 添加时间
    tag_id = db.Column(db.Integer, db.ForeignKey("album_tag.id"))  # 定义外键 tag_id 来源于album_tag表中id一个标签可有多个相册
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 定义外键 user_id 来源于 user表中id 一个用户可有多个相册
    favors = db.relationship("AlbumFavor", backref="album")  # 定义相册与收藏相册关系 通过收藏表的album_id 反向查找到相册
    photos = db.relationship("Photo", backref="album")  # 定义相册与图片关系 通过图片表的album_id 反向查找到相册

    def __repr__(self):
        return '<Album %r>' % (self.title)


# 用户收藏相册表
class AlbumFavor(db.Model):
    __tablename__ = "album_favor"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 定义外键 user_id 来源于 user表中id 一个用户可有多个收藏相册
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))  # 定义外键 album_id 来源于 album表中id 通过album_id获取到当前相册
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 收藏时间

    def __repr__(self):
        return '<AlbumFavor %r>' % (self.title)


class Photo(db.Model):
    __tablename__ = "photo"
    id = db.Column(db.Integer, primary_key=True)
    origname = db.Column(db.String(255), unique=True, nullable=False)  # 原图片名
    showname = db.Column(db.String(255), unique=True, nullable=False)  # 展示图片名
    thumbname = db.Column(db.String(255), unique=True, nullable=False)  # 缩略图片名
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"))  # 定义外键 album_id 来源于 album表中id 通过album_id获取到当前相册
    addtime = db.Column(db.DATETIME, index=True, default=datetime.now)  # 收藏时间


if __name__ == '__main__':
    # 当我们在数据库中写入新的类(表)或者某一表中添加或删除某一属性后需要更新数据库时，
    # 需要将__init__.py脚本中import apps.views 包注释掉，防止循环引用
    flag = 1
    if flag == 0:
        db.drop_all(bind=None)
        db.create_all()
    if flag == 1:
        tag0 = AlbumTag(name="沙漠")
        tag1 = AlbumTag(name="动漫")
        tag2 = AlbumTag(name="星空")
        tag3 = AlbumTag(name="萌宠")
        tag4 = AlbumTag(name="人物")
        tag5 = AlbumTag(name="植物")
        tag6 = AlbumTag(name="海洋")
        tag7 = AlbumTag(name="汽车")
        tag8 = AlbumTag(name="昆虫")
        tag9 = AlbumTag(name="飞鸟")
        tag10 = AlbumTag(name="花卉")
        tag11 = AlbumTag(name="美食")
        tag12 = AlbumTag(name="美食")
        tag12 = AlbumTag(name="森林")
        db.session.add(tag0)
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.add(tag3)
        db.session.add(tag4)
        db.session.add(tag5)
        db.session.add(tag6)
        db.session.add(tag7)
        db.session.add(tag8)
        db.session.add(tag9)
        db.session.add(tag10)
        db.session.add(tag11)
        db.session.add(tag12)
        db.session.commit()
