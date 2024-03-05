from flask import Flask
from flask import url_for
app = Flask(__name__)

# route for home "/"
@app.route("/")
def index():
    return 'Hello world!'

# route for "/about"
@app.route("/about")
def abaout():
    return 'This is the about page for this flask app'

# post folder route in fs
@app.route("/posts/")
def posts():
    return 'This is where the posts will be ...'

# dynamic route for viewing blog posts by post ID
@app.route("/posts/<int:post_id>")
def post_id():
    # logic to recieve and display blog post with given post ID
    return f'Blog Post #{post_id}'

#  a user profile that accepts a variable username
@app.route("/user/<username>")
def user_profile(username):
    # display user profile based on username
    return f'{username}\'s profile'

# generate a url for user_profile endpoint w username alice
with app.test_request_context():
    print(url_for('user_profile', username='alice'))

if __name__ == '__main__':
    app.run()