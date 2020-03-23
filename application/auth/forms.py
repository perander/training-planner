from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, validators


class LoginForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=2)])
    password = PasswordField("Password", [validators.Length(min=2)])

    class Meta:
        csrf = False


class RegisterForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=2)])
    password = PasswordField("Password", [validators.Length(min=2)])
    admin = BooleanField("Admin")

    class Meta:
        csrf = False
