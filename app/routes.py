from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app import db
from app.models import User
from urllib.parse import urlsplit

@app.route('/')
@app.route('/index')
@login_required
def index():
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
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # in case the user is already logged in they are redirected to index
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # load user from db
        user = db.session.scalar(
            # query the db w form submission info to find user
            sa.select(User).where(User.username == form.username.data))
        # check the password provided by the form
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # register user as logged in 
        # current user var is set to logged in user
        login_user(user, remember=form.remember_me.data)
        # redirect back from the successful login to the page the user wanted to access
        next_page = request.args.get('next')
        # to determine if the URL is absolute or relative
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))