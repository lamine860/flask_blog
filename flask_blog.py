from flask import Flask, render_template as render

from forms import RegistrationFrom

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form =  RegistrationFrom()
    return render('register.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)