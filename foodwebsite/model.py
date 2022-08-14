from . import db ,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))



class User(db.Model , UserMixin):
    id = db.Column(db.Integer , primary_key = True)
    username = db.Column(db.String(30) , nullable = False)
    email = db.Column(db.String(50) , nullable = False , unique = True )
    image_file = db.Column(db.String(50) , nullable= False , default = 'default.png')
    password = db.Column(db.String(50) , nullable = False )
    city = db.Column(db.String(30))

    restaurant = db.relationship('Restaurant' , backref = 'author',lazy = True)
    order = db.relationship('Orders' , backref = 'order_by',lazy = True)
    cart = db.relationship('Cart' , backref = 'placed_by',lazy = True)


class Restaurant(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    restaurant_name = db.Column(db.String(50) , nullable = False)
    image_file = db.Column(db.String(50) , nullable = False)
    street = db.Column(db.String(150) , nullable= False)
    city = db.Column(db.String(40) , nullable = False)

    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)

    items = db.relationship('Items' , backref = 'owner' , lazy = True)
    order = db.relationship('Orders' , backref = 'order_at',lazy = True)
    cart = db.relationship('Cart' , backref = 'placed_at',lazy = True)


class Items(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    item_name = db.Column(db.String(50) , nullable = False)
    item_image = db.Column(db.String(50) , nullable =False)
    item_category = db.Column(db.String(50) , nullable = False)
    item_price = db.Column(db.String(20) , nullable = False)

    restaurant_id = db.Column(db.Integer , db.ForeignKey('restaurant.id') , nullable = False)

    order = db.relationship('Orders' , backref = 'ordered',lazy = True)
    cart = db.relationship('Cart' , backref = 'placed',lazy = True)





class Cart(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    quantity = db.Column(db.String(50) , nullable =False)
    restaurant_id = db.Column(db.Integer , db.ForeignKey('restaurant.id') , nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    item_id = db.Column(db.Integer , db.ForeignKey('items.id') , nullable = False)


class Orders(db.Model):
    id = db.Column(db.Integer , primary_key = True)
    invoice = db.Column(db.Integer  ,nullable = False )
    quantity = db.Column(db.String(50) , nullable =False)
    orderStatus = db.Column(db.String(50), nullable = False ,default = 'Pending' )

    restaurant_id = db.Column(db.Integer , db.ForeignKey('restaurant.id') , nullable = False)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id') , nullable = False)
    item_id = db.Column(db.Integer , db.ForeignKey('items.id') , nullable = False)