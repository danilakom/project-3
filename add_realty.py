from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, IntegerField, StringField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired


class Add_Realty(FlaskForm):
    realtor = StringField('Имя и фамилия риэлтора', validators=[DataRequired()])
    house = StringField('Описание дома', validators=[DataRequired()])
    not_solded_flats = IntegerField("Сколько квартир не продано?", validators=[DataRequired()])
    address = StringField("Адрес", validators=[DataRequired()])
    cost = IntegerField("Сколько стоит одна квартира в среднем?")
    is_sold = BooleanField('Всё продано?')
    photo = FileField("Добавьте фото дома")
    submit = SubmitField('Добавить')