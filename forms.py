from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo



class RegistrationFrom(FlaskForm):
    
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password =  PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('password confirmation', validators=[EqualTo('password')])
    submit = SubmitField('Sign up')



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')