from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired


class RaceForm(FlaskForm):
    name = SelectField("Выбор расы",choices=[],validators=[DataRequired()])
    build_icon = FileField("Добавить изображение зданий", validators=[FileRequired()])
    vehicle_icon = FileField("Добавить изображение техники", validators=[FileRequired()])
    submit = SubmitField("Добавить")


class UnitForm(FlaskForm):
    name = StringField("Название юнита", validators=[DataRequired()])
    race_id = SelectField("Выбрать расу", choices=[], validators=[DataRequired()])
    icon = FileField("Добавить иконку", validators=[FileRequired()])
    submit = SubmitField("Добавить")

class BuildingForm(FlaskForm):
    name = StringField("Название здания", validators=[DataRequired()])
    race_id = SelectField("Выбрать расу", choices=[], validators=[DataRequired()])
    icon = FileField("Добавить иконку", validators=[FileRequired()])
    submit = SubmitField("Добавить")

class VehicleForm(FlaskForm):
    name = StringField("Название юнита", validators=[DataRequired()])
    race_id = SelectField("Выбрать расу", choices=[], validators=[DataRequired()])
    icon = FileField("Добавить иконку", validators=[FileRequired()])
    submit = SubmitField("Добавить")