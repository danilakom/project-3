from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    surname = StringField("Фамилия")
    name = StringField("Имя")
    age = IntegerField("Возраст")
    is_realtor = BooleanField("Вы риэлтор?", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    phone = StringField("Номер телефона")
    password = PasswordField("Password", validators=[DataRequired()])
    r_password = PasswordField("Repeat password", validators=[DataRequired()])
    submit = SubmitField("Submit")