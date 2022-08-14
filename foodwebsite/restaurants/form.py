from flask_wtf import FlaskForm
from wtforms import StringField   , SubmitField  
from wtforms.validators import   DataRequired , Email , Length , ValidationError
from flask_wtf.file import FileField , FileAllowed



class AddRestaurantForm(FlaskForm):
    restaurant_name = StringField('Restaurant Name' , validators = [DataRequired() , Length(min = 2  , max = 20)])
    picture = FileField('Restaurant Picture', validators=[FileAllowed(['jpg', 'png'])])
    street = StringField('street' , validators = [DataRequired() ])
    city = StringField('City' , validators = [DataRequired()])
    submit = SubmitField('Add Restaurant')

class UpdateRestaurantForm(FlaskForm):
    restaurant_name = StringField('restaurant_name' , validators = [DataRequired() , Length(min = 2  , max = 20)])
    picture = FileField('Update Restaurant Picture', validators=[FileAllowed(['jpg', 'png'])])
    street = StringField('street' , validators = [DataRequired() ])
    city = StringField('City' , validators = [DataRequired()])
    submit = SubmitField('Update Restaurant')


class AddItemsForm(FlaskForm):
    name = StringField('Name' , validators = [DataRequired() , Length(min=2 , max =20)])
    image_file = FileField('Image' , validators = [ FileAllowed(['jpg' , 'png'])])
    category = StringField('Category' , validators = [DataRequired()])
    price = StringField('Price' , validators = [DataRequired()])
    submit = SubmitField('Add Item')


class UpdateItemsForm(FlaskForm):
    name = StringField('Name' , validators = [DataRequired() , Length(min=2 , max =20)])
    image_file = FileField('Image' , validators = [ FileAllowed(['jpg' , 'png'])])
    category = StringField('Category' , validators = [DataRequired()])
    price = StringField('Price' , validators = [DataRequired()])
    submit = SubmitField('Update Item')