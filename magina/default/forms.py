from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(4, 20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Repeat password',
                                     validators=[DataRequired(), EqualTo('password', message='Password must match')])
    submit = SubmitField('Signup')


class KeywordForm(FlaskForm):
    keyword = StringField('', validators=[DataRequired()])
    submit = SubmitField('Add new keyword')
