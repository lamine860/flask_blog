import secrets 
import os
from PIL import Image
from flask import url_for, flash, render_template as render, redirect, request
from flask_login import login_required, login_user, logout_user, current_user


from flask_blog import app, bcrypt, db
from flask_blog.forms import RegistrationFrom, LoginForm, UpdateAccount
from flask_blog.models import User


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route('/')
def home():
    return render('home.html', posts=posts)


@app.route('/about')
def about():
    return render('about.html', title='About')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationFrom()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! Your are now able to login', 'success')
        return redirect(url_for('home'))

    return render('sign_up.html', form=form, title='Sign Up')



@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('You have been logged in!', 'success')
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')    
    return render('sign_in.html', form=form, title='Sign In')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_picture/' + picture_fn )
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


    

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccount()
    if form.validate_on_submit():
        if form.picture.data:
            image_file = save_picture(form.picture.data)
        current_user.username = form.username.data 
        current_user.email= form.email.data 
        current_user.image_file=image_file
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    if not current_user.image_file:
        image_file = url_for('static', filename='profile_picture/' + 'default.jpeg')
    else:
        image_file = url_for('static', filename='profile_picture/' + current_user.image_file)
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render('account.html', title='Account', form=form, image_file=image_file)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))