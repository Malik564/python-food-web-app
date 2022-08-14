from flask import Blueprint , render_template  , redirect , url_for
from foodwebsite.model import Items, Restaurant , Cart,Orders
from foodwebsite import db
from flask_login import current_user
import random

cart = Blueprint('cart' , __name__ )

@cart.route('/restaurant/<int:res_id>/item/<int:item_id>/qty/<int:qty>/add_to_cart' , methods = ['GET' , 'POST'])
def add_to_cart(res_id , item_id,qty):
    restaurant = Restaurant.query.get(res_id)
    c = Cart.query.filter_by(placed_at = restaurant).filter_by(placed_by = current_user)
    for ca in c :
        if ca.placed.id == item_id:
            ca.quantity = int(ca.quantity) + qty
            db.session.commit()
            return redirect(url_for('restaurants.restaurant_menu'  , id = res_id))
            
    cart = Cart(quantity = qty , restaurant_id = res_id , user_id = current_user.id , item_id = item_id)
    db.session.add(cart)
    db.session.commit()
    return redirect(url_for('restaurants.restaurant_menu'  , id = res_id))


@cart.route('/restaurant/<int:res_id>/cart' , methods = ['GET' ] )
def cart_data(res_id):
    restaurant = Restaurant.query.get(res_id)
    cart = Cart.query.filter_by(placed_at = restaurant).filter_by(placed_by = current_user)
    total = 0
    for c in cart:
        total = total + (int(c.placed.item_price) * int(c.quantity))
    return render_template('cart.html' , title = 'Cart' , cart = cart , restaurant = restaurant ,total = total)


@cart.route('/restaurant/<int:res_id>/cart/<int:cart_id>/delete' , methods = [ 'GET','POST'])
def delete_cart_item(res_id , cart_id):
    restaurant = Restaurant.query.get(res_id)
    cart = Cart.query.filter_by(placed_at = restaurant).filter_by(placed_by = current_user)
    for c in cart:
        if c.id == cart_id:
            db.session.delete(c)
            db.session.commit()
            return redirect(url_for('cart.cart_data' , res_id = restaurant.id ))
    return render_template('cart.html' , title = 'Cart' , cart = cart , restaurant = restaurant)


@cart.route('/restaurant/<int:res_id>/cart/proceed_order' , methods = [ 'GET','POST'])
def proceed_order(res_id  ):
    restaurant = Restaurant.query.get(res_id)
    cart = Cart.query.filter_by(placed_at = restaurant).filter_by(placed_by = current_user)
    invoice = random.randint(10000,1000000)
    for c in cart:
        order = Orders(invoice = invoice, quantity = c.quantity , restaurant_id = res_id , user_id = current_user.id , item_id = c.placed.id )    
        db.session.add(order)
    db.session.commit()

    for c in cart:
        db.session.delete(c)
    db.session.commit()
    return redirect(url_for('restaurants.restaurant_menu' , id=res_id))