from flask_uploads import IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Regexp   # Regexp正则表达式验证器
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RegistForm(FlaskForm):
    user_name = StringField(
        label="用户名：",
        validators=[DataRequired(message="用户名不能为空！"),
                    Length(min=3, max=15, message="用户名长度3-15个字符")],
        render_kw={"id": "user_name",
                   "calss": "form-control",
                   "placeholder": "输入用户名"
                   }
    )

    user_pwd = PasswordField(
        label="用户密码：",
        validators=[DataRequired(message="用户密码不能为空！"),
                    Length(min=3, max=5, message="用户密码长度3-5个字符")],
        render_kw={"id": "user_pwd",
                   "calss": "form-control",
                   "placeholder": "输入密码"
                   }
    )

    user_email = StringField(
        label="用户邮箱：",
        validators=[DataRequired(message="用户邮箱不能为空！"),
                    Email(message="邮箱格式错误！")],
        render_kw={"id": "user_email",
                   "calss": "form-control",
                   "placeholder": "输入用户邮箱"
                   }
    )

    user_phone = StringField(

        label="用户手机：",
        validators=[DataRequired(message="用户手机不能为空！"),
                    Regexp("1[1,2,3,5,6,7,8,9]\d{9}",message="手机号格式不正确！")],
        render_kw={"id": "user_phone",
                   "calss": "form-control",
                   "placeholder": "输入用户手机"
                   }
    )

    user_face = FileField(
        label="用户头像：",
        validators=[FileRequired(message="用户头像不能为空！"),
                    FileAllowed(IMAGES, "只允许图像格式为：%s" % str(IMAGES))],
        render_kw={"id": "user_face",
                   "calss": "form-control",
                   "placeholder": "选择头像"
                   }
    )

    user_jianjie = TextAreaField(

        label="用户简介",
        validators=[],
        render_kw={"id": "user_jianjie",
                   "calss": "form-control",
                   "placeholder": "用户简介"
                   }
    )


    submit = SubmitField(
        label="提交表单",
        render_kw={"class": "btn-success",
                   "value": "注册"
                   }
    )


class LoginForm(FlaskForm):
    user_name = StringField(
        label="用户名：",
        validators=[DataRequired(message="用户名不能为空！")],
        render_kw={"id": "user_name",
                   "calss": "form-control",
                   "placeholder": "输入用户名"
                   }
    )

    user_pwd = PasswordField(
        label="用户密码：",
        validators=[DataRequired(message="用户密码不能为空！")],
        render_kw={"id": "user_pwd",
                   "calss": "form-control",
                   "placeholder": "输入密码"
                   }
    )
    submit = SubmitField(
        label="提交表单",
        render_kw={"class": "btn-success",
                   "value": "登录"
                   }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="用户旧密码：",
        validators=[DataRequired(message="用户密码不能为空！")],
        render_kw={"id": "old_pwd",
                   "calss": "form-control",
                   "placeholder": "输入密码"
                   }
    )

    new_pwd = PasswordField(
        label="用户新密码：",
        validators=[DataRequired(message="用户密码不能为空！"),
                    Length(min=3, max=5, message="用户密码长度3-5个字符")],
        render_kw={"id": "new_pwd",
                   "calss": "form-control",
                   "placeholder": "输入密码"
                   }
    )

    submit = SubmitField(
        label="提交表单",
        render_kw={"class": "btn-success",
                   "value": "修改"
                   }
    )


class InfoForm(FlaskForm):
    user_name = StringField(
        label="用户名：",
        validators=[DataRequired(message="用户名不能为空！"),
                    Length(min=3, max=15, message="用户名长度3-15个字符")],
        render_kw={"id": "user_name",
                   "calss": "form-control",
                   "placeholder": "输入用户名"
                   }
    )

    user_email = StringField(
        label="用户邮箱：",
        validators=[DataRequired(message="用户邮箱不能为空！"),
                    Email(message="邮箱格式错误！")],
        render_kw={"id": "user_email",
                   "calss": "form-control",
                   "placeholder": "输入用户邮箱"
                   }
    )

    user_phone = StringField(

        label="用户手机：",
        validators=[DataRequired(message="用户手机不能为空！")],
        render_kw={"id": "user_phone",
                   "calss": "form-control",
                   "placeholder": "输入用户手机"
                   }
    )

    user_jianjie = TextAreaField(

        label="用户简介",
        validators=[],
        render_kw={"id": "user_jianjie",
                   "calss": "form-control",
                   "placeholder": "用户简介"
                   }
    )


    user_face = FileField(
        label="用户头像：",
        validators=[FileAllowed(IMAGES, "只允许图像格式为：%s" % str(IMAGES))],
        render_kw={"id": "user_face",
                   "calss": "form-control",
                   "placeholder": "选择头像"
                   }
    )

    submit = SubmitField(
        label="提交表单",
        render_kw={"class": "btn-success",
                   "value": "修改"
                   }
    )
