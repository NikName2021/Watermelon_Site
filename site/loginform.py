from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class AddPhrase(FlaskForm):
    phrase = StringField('Фраза', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class DelPhrase(FlaskForm):
    phrase = StringField('Номер записи', validators=[DataRequired()])
    submit = SubmitField('Удалить')


class DelUser(FlaskForm):
    phrase = StringField('Логин', validators=[DataRequired()])
    submit = SubmitField('Удалить')


class AddUser(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    is_admin = BooleanField('Назначить администратором')
    submit = SubmitField('Добавить')
