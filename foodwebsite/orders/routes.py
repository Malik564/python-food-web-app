from flask import Blueprint , render_template ,redirect , url_for , request
from foodwebsite.model import Orders, Restaurant
from foodwebsite import db
from flask_login import current_user

orders  = Blueprint('orders', __name__)


@orders.route('/orders/' )
def all_orders():
    restaurant = Restaurant.query.filter_by(user_id = current_user.id).first()
    if restaurant:
        orders = Orders.query.filter_by(order_at = restaurant)
        return render_template('orders.html' , title = 'Orders' , restaurant = restaurant  , orders = orders)
    else:
        return redirect(url_for('restaurants.my_restaurant'))

@orders.route('/orders/<int:inv>' , methods =['GET' ,'POST'] )
def order_data(inv):
    restaurant = Restaurant.query.filter_by(user_id = current_user.id).first()

    if restaurant:
        orders = Orders.query.filter_by(order_at = restaurant).filter_by(invoice = inv)
        
        if request.method == 'POST':
            print(request.args.get("StatusSelecter"))
            for order in orders:
                order.orderStatus = request.form.get("StatusSelecter")
            db.session.commit()
            
        return render_template('order.html' , title = 'Orders' , restaurant = restaurant  , orders = orders)
    else:
        return redirect(url_for('restaurants.my_restaurant'))
