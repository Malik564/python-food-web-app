from flask import Blueprint , render_template 
from .model import Items, Restaurant 

views = Blueprint('views' , __name__)



@views.route('/' , methods = ['GET'])
def home():
    restaurants = Restaurant.query.all()
    return render_template('home.html' , title = 'Home' , restaurants = restaurants)



restaurants =[
    {'restaurant_name' : 'zfc',
    'image_file' : 'static/profiles/0a7b4165fe6d3867.png',
     'street': 'main road',
     'city' : 'Narowal'},
     
     {'restaurant_name' : 'crunch bite',
     'street': 'circular road',
     'city' : 'Narowal'},

     {'restaurant_name' : 'folk and knives',
     'street': 'zafarwal chowk',
     'city' : 'Narowal'}
]






@views.route('/about' )
def about():
    return render_template('about.html' , title = 'About')
    
    
@views.route('/faqs' )
def faqs():
    return render_template('FAQs.html' , title = 'FAQs')