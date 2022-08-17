from flask import Blueprint , render_template , flash , request , redirect , url_for , abort
from flask_login import current_user , login_required
from foodwebsite.restaurants.form import AddItemsForm, AddRestaurantForm, UpdateItemsForm , UpdateRestaurantForm
from foodwebsite.model import Restaurant ,Items, Cart
from foodwebsite import db
from foodwebsite.utils import save_picture

restaurants = Blueprint('restaurants' , __name__)




@restaurants.route('/my_restaurant' , methods = ['GET','POST'] )
@login_required
def my_restaurant():
    form = AddItemsForm()
    restaurant = Restaurant.query.filter_by(user_id = current_user.id).first()
    items = Items.query.filter_by(owner = restaurant).all()
    if restaurant:
        image_file = url_for("static" , filename ='restaurants/' + restaurant.image_file)

        if form.validate_on_submit():
            item_picture =''
            if form.image_file.data:
                item_picture = save_picture(form.image_file.data , 'restaurants')

            item = Items(item_name = form.name.data ,item_image = item_picture , item_category = form.category.data , item_price = form.price.data ,restaurant_id = restaurant.id )
            db.session.add(item)
            db.session.commit()

            return redirect(url_for('restaurants.my_restaurant'))
        return render_template('my_restaurant.html' , title = 'My Restaurant' , restaurant = restaurant , image_file = image_file , form = form , items = items) 
    
    return render_template('my_restaurant.html' , title = 'My Restaurant' , restaurant = restaurant )





@restaurants.route('/restaurant/add' , methods = ['GET' , 'POST'] )
@login_required
def add_restaurant():
    form = AddRestaurantForm()
    picture_file = ''
    if form.validate_on_submit():
        print(form.picture.data)
        if form.picture.data:
            picture_file = save_picture(form.picture.data , 'restaurants') 
        restaurant = Restaurant(restaurant_name = form.restaurant_name.data , image_file =picture_file , street = form.street.data , city = form.city.data , user_id = current_user.id )
        db.session.add(restaurant)
        db.session.commit()
        flash(f'Restaurant has been added successfully ! ' , 'success')
        return redirect(url_for('restaurants.my_restaurant' ))
    return render_template('add_restaurant.html' , title = 'Add Restaurant' ,form = form )





@restaurants.route('/restaurant/update' , methods = ['GET' , 'POST'] )
@login_required
def edit_restaurant():
    
    restaurant = Restaurant.query.filter_by(user_id = current_user.id).first()
    if not restaurant:
        return redirect(url_for('restaurants.my_restaurant'))

    form = UpdateRestaurantForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data , 'restaurants') 
            restaurant.image_file = picture_file

        restaurant.restaurant_name = form.restaurant_name.data
        restaurant.street = form.street.data
        restaurant.city = form.city.data

        db.session.commit()
        flash(f'Restaurant has been updated successfully ! ' , 'success')
        return redirect(url_for('restaurants.my_restaurant' ))

    elif request.method =='GET':
        form.restaurant_name.data = restaurant.restaurant_name
        form.picture.data = restaurant.image_file
        form.street.data = restaurant.street
        form.city.data= restaurant.city
    
    return render_template('edit_restaurant.html' , title = 'Add Restaurant' ,form = form  )



@restaurants.route('/restaurant/delete' , methods = ['POST'] )
@login_required
def delete_restaurant():
    restaurant = Restaurant.query.get(current_user.id)
    if restaurant.author != current_user:
        abort(403)
    db.session.delete(restaurant)
    db.session.commit()
    flash(f'Your restaurant is been deleted !' ,'success')
    return redirect(url_for('view.home'))




@restaurants.route('/my_restaurant/<int:item_id>/delete' ,methods =['POST'])
@login_required
def delete_item(item_id):
    item = Items.query.get(item_id)
    res = Restaurant.query.get(current_user.id)
    if item.owner != res:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash(f'Your Item is been deleted !' ,'success')
    return redirect(url_for('restaurants.my_restaurant'))



@restaurants.route('/my_restaurant/<int:item_id>/edit' ,methods =['GET','POST'])
@login_required
def edit_item(item_id):
    item = Items.query.get(item_id)
    form = UpdateItemsForm()
    res = Restaurant.query.get(current_user.id)
    if item.owner != res:
        abort(403)

    if form.validate_on_submit():
        picture_file=''
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data , 'restaurants')
            item.item_image = picture_file
        item.item_name = form.name.data
        item.item_category = form.category.data
        item.item_price = form.price.data
        db.session.commit()

        flash(f'Your Item is been updatedd !' ,'success')
        return redirect(url_for('restaurants.my_restaurant'))
    elif request.method == 'GET':
        form.name.data = item.item_name
        form.category.data = item.item_category
        form.price.data = item.item_price 
    return render_template('edit_item.html' , form = form   )





@restaurants.route('/restaurant/<int:id>/menu' , methods = ['GET' , 'POST'])
def restaurant_menu(id):
    
    restaurant = Restaurant.query.get(id)
    if restaurant:
        items = Items.query.filter_by( owner = restaurant)
        cart_count = 0
        if current_user.is_authenticated:
            cart_count = Cart.query.filter_by(placed_by = current_user).filter_by(placed_at = restaurant).count()
        
        if request.method == 'POST':
            quantity = request.form['quantity']
            item_id = request.form['itemId']
            return redirect(url_for('cart.add_to_cart' ,res_id= restaurant.id,  item_id = item_id , qty = quantity , cart_count = cart_count))
        return render_template('restaurant_menu.html' , restaurant = restaurant , items = items , cart_count = cart_count)
