from flask import Blueprint , render_template , flash , request , redirect , url_for 
from flask_login import current_user , login_required
from foodwebsite.user.form import  UpdateAccountForm
from foodwebsite import db
from foodwebsite.utils import save_picture

users = Blueprint('users' , __name__)


@users.route('/account')
@login_required
def account():
    image_file = url_for("static" , filename ='profiles/' + current_user.image_file) 
    return render_template('account.html' , title = current_user.username , image_file = image_file)




@users.route('/account/update' , methods= ['GET' , 'POST'])
@login_required
def edit_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data , 'profiles')
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.city = form.city.data

        db.session.commit()
        flash('Your account has been apdated' , 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET' :
        form.username.data= current_user.username
        form.email.data = current_user.email
        form.city.data = current_user.city
        form.picture.data= current_user.image_file 

    image_file = url_for("static" , filename ='profiles/' + current_user.image_file) 
    return render_template('edit_account.html' , title = current_user.username , form = form , image_file = image_file)

