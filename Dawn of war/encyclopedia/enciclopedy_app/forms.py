from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class RaceForm(FlaskForm):
    name = StringField("Название расы", validators=[DataRequired(message='Обязательное поле')])
    build_icon = StringField("Ссылка на изображение зданий", validators=[DataRequired(message='Обязательное поле')])
    vehicle_icon = StringField("Ссылка на изображение техники", validators=[DataRequired(message='Обязательное поле')])
    submit = SubmitField("Добавить")
