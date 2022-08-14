from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , BooleanField 
from wtforms.validators import EqualTo , DataRequired , Email , Length , ValidationError
from flask_wtf.file import FileField , FileAllowed


class RegisterationForm(FlaskForm):
    username = StringField('Username' , validators = [DataRequired() , Length(min = 2  , max = 20)])
    email = StringField('Email' , validators = [DataRequired() , Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    password = PasswordField('Password'  , validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password' , validators=[DataRequired() , EqualTo('password') ])
    city = StringField('City' , validators = [DataRequired()])
    submit = SubmitField('Register')



class LoginForm(FlaskForm):
    email = StringField('Email' , validators = [DataRequired() , Email()])
    password = PasswordField('Password'  , validators = [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')