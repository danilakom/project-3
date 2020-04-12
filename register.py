from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    surname = StringField("Фамилия")
    name = StringField("Имя")
    age = IntegerField("Возраст")
    is_realtor = BooleanField("Вы риелтор?")
    email = EmailField("Email", validators=[DataRequired()])
    phone = StringField("Номер телефона")
    password = PasswordField("Пароль", validators=[DataRequired()])
    r_password = PasswordField("Повторите пароль", validators=[DataRequired()])
    submit = SubmitField("Submit")