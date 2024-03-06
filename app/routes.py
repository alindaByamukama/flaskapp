from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Susan'}
    return '''
<html>
    <head>
        <title>Home Page - Flaskblog</title>
    </head>
    <body>
        <h1>Welcome, ''' + user['username'] + '''!</h1>
    </body>
</html>'''