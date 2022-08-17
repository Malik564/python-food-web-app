from flask import Blueprint , render_template ,redirect , url_for , request
from foodwebsite.model import Orders, Restaurant
from foodwebsite import db
from flask_login import current_user,login_required

orders  = Blueprint('orders', __name__)


@orders.route('/orders/' )
@login_required
def all_orders():
    restaurant = Restaurant.query.filter_by(user_id = current_user.id).first()
    if restaurant:
        orders = Orders.query.filter_by(order_at = restaurant).group_by('invoice')
        return render_template('orders.html' , title = 'Orders' , restaurant = restaurant  , orders = orders)
    else:
        return redirect(url_for('restaurants.my_restaurant'))



@orders.route('/orders/<int:inv>' , methods =['GET' ,'POST'] )
@login_required
def order_data(inv):
    restaurant = Restaurant.query.filter_by(user_id = current_user.id).first()

    if restaurant:
        orders = Orders.query.filter_by(order_at = restaurant).filter_by(invoice = inv)
        total = 0
        for o in orders:
            total = total + (int(o.ordered.item_price) * int(o.quantity))

        if request.method == 'POST':
            print(request.args.get("StatusSelecter"))
            for order in orders:
                order.orderStatus = request.form.get("StatusSelecter")
            db.session.commit()
            
        return render_template('order.html' , title = 'Orders' , restaurant = restaurant  , orders = orders , total = total)
    else:
        return redirect(url_for('restaurants.my_restaurant'))




@orders.route('/my_orders')
@login_required
def my_orders():
    orders = Orders.query.filter_by(order_by = current_user).group_by('invoice')
    return render_template('my_orders.html'  , title='My Orders' , orders = orders )




@orders.route('/my_order/<int:inv>' , methods =['GET' ,'POST'] )
@login_required
def my_order(inv):
    orders = Orders.query.filter_by(order_by = current_user).filter_by(invoice = inv)
    total = 0
    for o in orders:
        total = total + (int(o.ordered.item_price) * int(o.quantity))
    return render_template('my_order.html'  , title='My Orders' , orders = orders,total = total )