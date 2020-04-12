from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class Add_Realty(FlaskForm):
    realtor = StringField('Имя и фамилия риелтора', validators=[DataRequired()])
    house = StringField('Описание', validators=[DataRequired()])
    not_solded_flats = IntegerField("Свободных квартир")
    address = StringField("Адрес", validators=[DataRequired()])
    cost = IntegerField("Средняя стоимость квартиры")
    photo = FileField("Добавить фото дома")
    submit = SubmitField('Добавить')