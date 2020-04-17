from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, IntegerField, StringField, MultipleFileField, TextAreaField
from wtforms.validators import DataRequired


class Add_Realty(FlaskForm):
    realtor = StringField('Имя и фамилия риелтора', validators=[DataRequired()])
    house = BooleanField('Дом')
    desc = TextAreaField('Описание')
    address = StringField("Адрес", validators=[DataRequired()])
    cost = IntegerField("Стоимость")
    photo = MultipleFileField("Добавить фото")
    submit = SubmitField('Добавить')