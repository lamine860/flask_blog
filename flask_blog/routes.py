import secrets 
import os
from PIL import Image
from flask import url_for, flash, render_template as render, redirect, request, abort
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message

from flask_blog import app, bcrypt, db, mail
from flask_blog.forms import RegistrationFrom, LoginForm, UpdateAccount, PostForm, RequestResetForm, ResetPasswordForm
from flask_blog.models import User, Post




@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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
    picture_path = os.path.join(app.root_path, 'static/profile_pics/' + picture_fn )
    
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
        image_file = url_for('static', filename='profile_pics/' + 'default.jpeg')
    else:
        image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render('account.html', title='Account', form=form, image_file=image_file)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render('new_post.html', title='New Post', form=form)



@app.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render('post.html', title='Post', post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render('new_post.html', title='Update Post',
                           form=form, legend='Update Post')
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

def send_reset(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='noreply@geek4020m.com',recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: <a href="{url_for('reset_token', token=token, _external=True)}">Reset Password</a>
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)
    


@app.route('/request_reset', methods=['GET', 'POST'])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url('home'))    
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset(user)
        flash('An email has been send with instructions to reset your password.', 'success')
        return redirect(url_for('sign_in'))
    return render('request_reset.html', title='Request Reset', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! your now able to login.', 'success')
        return redirect(url_for('sign_in'))
    return render('reset_token.html', title='Reset Password', form=form)   