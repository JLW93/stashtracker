from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_email = StringField('Confirm Email', validators = [DataRequired(), Email()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired()])
    submit_button = SubmitField('Submit')

