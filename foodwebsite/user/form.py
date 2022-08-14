from flask_wtf import FlaskForm
from wtforms import StringField   , SubmitField  
from wtforms.validators import   DataRequired , Email , Length , ValidationError
from flask_wtf.file import FileField , FileAllowed




class UpdateAccountForm(FlaskForm):
    username = StringField('Username' , validators = [DataRequired() , Length(min = 2  , max = 20)])
    email = StringField('Email' , validators = [DataRequired() , Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    city = StringField('City' , validators = [DataRequired()])
    submit = SubmitField('Update')
