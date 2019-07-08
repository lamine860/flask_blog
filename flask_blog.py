from flask import Flask, render_template as render, flash, redirect, url_for

from forms import RegistrationFrom, LoginForm

posts = [
    {
        'title': 'The first post',
        'body': 'The body of the first post',
        'date_posted': '07/04/19',
        'author': 'Lamine Diallo',
    },
    {

        'title': 'The second post',
        'body': 'The body of the second post',
        'date_posted': '07/04/19',
        'author': 'Lamine Diallo',
    },
]
app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

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

    
if __name__ == '__main__':
    app.run(debug=True)