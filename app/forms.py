from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('Submit')

class Signup(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    submit = SubmitField('Submit')

class Blog(FlaskForm):
    message = StringField('message')
    submit = SubmitField('Submit')