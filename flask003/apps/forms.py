from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, Email, NumberRange


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

    user_age = IntegerField(

        label="用户年龄：",
        validators=[DataRequired(message="用户密码不能为空！"),
                    NumberRange(min=0, max=100, message="用户年龄在0~100范围")],
        render_kw={"id": "user_age",
                   "calss": "form-control",
                   "placeholder": "输入用户年龄"
                   }
    )

    user_birthday = StringField(
        label="用户生日：",
        validators=[DataRequired(message="用户生日不能为空！")],
        render_kw={"id": "user_birthday",
                   "calss": "form-control",
                   "placeholder": "输入用户生日"
                   }
    )

    user_face = FileField(
        label="用户头像：",
        validators=[DataRequired(message="用户头像不能为空！")],
        render_kw={"id": "user_face",
                   "calss": "form-control",
                   "placeholder": "选择头像"
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
        label="用户密码：",
        validators=[DataRequired(message="用户密码不能为空！")],
        render_kw={"id": "old_pwd",
                   "calss": "form-control",
                   "placeholder": "输入密码"
                   }
    )

    new_pwd = PasswordField(
        label="用户密码：",
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

    user_age = IntegerField(

        label="用户年龄：",
        validators=[DataRequired(message="用户密码不能为空！"),
                    NumberRange(min=0, max=100, message="用户年龄在0~100范围")],
        render_kw={"id": "user_age",
                   "calss": "form-control",
                   "placeholder": "输入用户年龄"
                   }
    )

    user_birthday = StringField(
        label="用户生日：",
        validators=[DataRequired(message="用户生日不能为空！")],
        render_kw={"id": "user_birthday",
                   "calss": "form-control",
                   "placeholder": "输入用户生日"
                   }
    )

    user_face = FileField(
        label="用户头像：",
        validators=[],
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
