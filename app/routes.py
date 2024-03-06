from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Susan'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beatiful day in Jinja!'
        },
        {
            'author': {'username': 'Martha'},
            'body': 'Just watched Dune at Cineplex, so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)