from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo

from flask_blog.models import User


posts = [
    {
        'title': 'The first post',
        'body': 'The body of the first post',
        'date_posted': '07/04/19',
        'author': 'Lamine Diallo',
    },
    {

        'title': 'The second post',
        'body': 'The body of the second post',
        'date_posted': '07/04/19',
        'author': 'Lamine Diallo',
    },
]

class RegistrationFrom(FlaskForm):
    
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password =  PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('password confirmation', validators=[EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken! Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken! Please choose a different one.')        



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')