from flask import url_for, flash, render_template as render
from flask_blog.forms import RegistrationFrom, LoginForm
from flask_blog import app


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
    form = RegistrationFrom()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render('sign_up.html', form=form, title='Sign Up')



@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.fr' and form.password.data == '0000':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')    
    return render('sign_in.html', form=form, title='Sign In')
