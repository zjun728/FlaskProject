
from flask_uploads import IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp  # Regexp正则表达式验证器
from flask_wtf.file import FileField, FileRequired, FileAllowed

from apps.models import AlbumTag, Album

album_tags = AlbumTag.query.all()  # 获取全部相册标签


class RegistForm(FlaskForm):
    user_name = StringField(
        label="用户名：",
        validators=[DataRequired(message="用户名不能为空！"),
                    Length(min=3, max=15, message="用户名长度3-15个字符")],
        render_kw={"id": "user_name",
                   "class": "form-control",
                   "placeholder": "输入用户名"
                   }
    )

    user_pwd = PasswordField(
        label="用户密码：",
        validators=[DataRequired(message="用户密码不能为空！"),
                    Length(min=3, max=5, message="用户密码长度3-5个字符")],
        render_kw={"id": "user_pwd",
                   "class": "form-control",
                   "placeholder": "输入密码"
                   }
    )

    user_email = StringField(
        label="用户邮箱：",
        validators=[DataRequired(message="用户邮箱不能为空！"),
                    Email(message="邮箱格式错误！")],
        render_kw={"id": "user_email",
                   "class": "form-control",
                   "placeholder": "输入用户邮箱"
                   }
    )

    user_phone = StringField(

        label="用户手机：",
        validators=[DataRequired(message="用户手机不能为空！"),
                    Regexp("1[3,5,6,7,8,9]\d{9}", message="手机号格式不正确！")],
        render_kw={"id": "user_phone",
                   "class": "form-control",
                   "placeholder": "输入用户手机"
                   }
    )

    user_face = FileField(
        label="用户头像：",
        validators=[FileRequired(message="用户头像不能为空！"),
                    FileAllowed(IMAGES, "只允许图像格式为：%s" % str(IMAGES))],
        render_kw={"id": "user_face",
                   "class": "form-control",
                   "placeholder": "选择头像"
                   }
    )

    user_jianjie = TextAreaField(

        label="用户简介",
        validators=[],
        render_kw={"id": "user_jianjie",
                   "class": "form-control",
                   "placeholder": "用户简介"
                   }
    )

    submit = SubmitField(
        label="提交表单",
        render_kw={"class": "btn btn-success",
                   "value": "注册"
                   }
    )


class LoginForm(FlaskForm):
    user_name = StringField(
        label="用户名：",
        validators=[DataRequired(message="用户名不能为空！")],
        render_kw={"id": "user_name",
                   "class": "form-control",
                   "placeholder": "输入用户名"
                   }
    )

    user_pwd = PasswordField(
        label="用户密码：",
        validators=[DataRequired(message="用户密码不能为空！")],
        render_kw={"id": "user_pwd",
                   "class": "form-control",
                   "placeholder": "输入密码"
                   }
    )
    submit = SubmitField(
        label="提交表单",
        render_kw={"class": "btn btn-success",
                   "value": "登录"
                   }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="用户旧密码：",
        validators=[DataRequired(message="用户密码不能为空！")],
        render_kw={"id": "old_pwd",
                   "class": "form-control",
                   "placeholder": "输入密码"
                   }
    )

    new_pwd = PasswordField(
        label="用户新密码：",
        validators=[DataRequired(message="用户密码不能为空！"),
                    Length(min=3, max=5, message="用户密码长度3-5个字符")],
        render_kw={"id": "new_pwd",
                   "class": "form-control",
                   "placeholder": "输入密码"
                   }
    )

    submit = SubmitField(
        label="提交表单",
        render_kw={"class": "btn btn-success",
                   "value": "修改"
                   }
    )


class InfoForm(FlaskForm):
    user_name = StringField(
        label="用户名：",
        validators=[DataRequired(message="用户名不能为空！"),
                    Length(min=3, max=15, message="用户名长度3-15个字符")],
        render_kw={"id": "user_name",
                   "class": "form-control",
                   "placeholder": "输入用户名"
                   }
    )

    user_email = StringField(
        label="用户邮箱：",
        validators=[DataRequired(message="用户邮箱不能为空！"),
                    Email(message="邮箱格式错误！")],
        render_kw={"id": "user_email",
                   "class": "form-control",
                   "placeholder": "输入用户邮箱"
                   }
    )

    user_phone = StringField(

        label="用户手机：",
        validators=[DataRequired(message="用户手机不能为空！"),
                    Regexp("1[3,5,6,7,8,9]\d{9}", message="手机号格式不正确！")],
        render_kw={"id": "user_phone",
                   "class": "form-control",
                   "placeholder": "输入用户手机"
                   }
    )

    user_jianjie = TextAreaField(

        label="用户简介",
        validators=[],
        render_kw={"id": "user_jianjie",
                   "class": "form-control",
                   "placeholder": "用户简介"
                   }
    )

    user_face = FileField(
        label="用户头像：",
        validators=[FileAllowed(IMAGES, "只允许图像格式为：%s" % str(IMAGES))],
        render_kw={"id": "user_face",
                   "class": "form-control",
                   "placeholder": "选择头像"
                   }
    )

    submit = SubmitField(
        label="提交表单",
        render_kw={"class": "btn btn-success",
                   "value": "修改"
                   }
    )


class AlbumInfoForm(FlaskForm):
    album_title = StringField(
        label="相册名称",
        validators=[DataRequired(message="相册名称不能为空！"),
                    Length(min=3, max=15, message="相册名称长度3-15个字符")],
        render_kw={"id": "album_title",
                   "class": "form-control",
                   "rows": "3",
                   "placeholder": "请输入相册名称"
                   }
    )

    album_desc = TextAreaField(
        label="相册描述",
        validators=[DataRequired(message="相册描述不能为空！"),
                    Length(min=10, max=200, message="相册描述长度10-200个字符")],
        render_kw={"id": "album_desc",
                   "class": "form-control",
                   "placeholder": "相册描述"
                   }
    )

    album_privacy = SelectField(
        label="相册浏览权限",
        validators=[DataRequired(message="相册浏览权限不能为空！")],
        coerce=str,
        choices=[("private", "仅自己"), ("protect_1", "粉丝可见"),
                 ("protect_2", "收藏者可见"), ("public", "所有人可见")],
        render_kw={"id": "album_privacy",
                   "class": "form-control",
                   }
    )

    album_tag = SelectField(
        label="相册类别标签",
        validators=[DataRequired(message="相册类别标签不能为空！")],
        coerce=int,

        choices=[(tag.id, tag.name) for tag in album_tags],  # 获取到数据库中存储的全部相册标签然后动态填写
        render_kw={"id": "album_tag",
                   "class": "form-control",
                   }
    )

    submit = SubmitField(
        label="创建相册信息",
        render_kw={"class": "btn btn-success",
                   "value": "创建相册信息"
                   }
    )


class AlbumUploadForm(FlaskForm):
    album_title = SelectField(
        validators=[DataRequired(message="相册名称不能为空！")],
        coerce=int,
        # choices=[(item.id, item.title) for item in albums],  # 获取到数据库中存储的全部相册标签然后动态填写
        render_kw={"id": "album_title", "class": "form-control"}
    )

    album_upload = FileField(
        # validators=[FileRequired(message="请选择一张或多张图片上传！"),
        #             FileAllowed(IMAGES, "只允许图像格式为：%s" % str(IMAGES))],
        # render_kw={"id": "album_upload", "class": "form-control", "multiple": "multiple"
        #            }
    )

    submit = SubmitField(
        render_kw={"class": "form-control btn btn-primary",
                   "value": "上传相册图片"
                   }
    )
