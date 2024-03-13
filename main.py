# a python script at the top level that defines the flask application instance
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post

# creates a shell context 
# adds the database instance and models to the shell session
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}