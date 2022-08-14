from flask import Blueprint , render_template , flash , url_for , redirect , request
from foodwebsite.auth.form import LoginForm, RegisterationForm
from foodwebsite import db , bcrypt
from foodwebsite.model import User
from flask_login import current_user , login_user , logout_user , login_required
from foodwebsite.utils import save_picture

auth = Blueprint('auth' , __name__)



@auth.route('/register',methods= ['GET', 'POST'] )
def register():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RegisterationForm()
    picture_file = 'default.png'
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data , 'profiles')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data , email = form.email.data ,image_file= picture_file,  password = hashed_password , city = form.city.data)
        db.session.add(user)
        db.session.commit()
        
        flash(f'Account created for {form.username.data}!' , 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html' , title= 'Register' ,form = form )





@auth.route('/login',methods= ['GET', 'POST'] )
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form= LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password , form.password.data):
            login_user(user , remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else :
            flash(f'User email or password is invalid' , 'danger')
    return render_template('login.html' , title= 'Login' ,form = form )


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))
