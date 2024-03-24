from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from hashlib import md5

# user loader is registered with flask login with this decorator
@login.user_loader
# the id being passed as an arg is a str
def user_loader(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    # the optional helper from python allows for a col to be empty or nullable
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    # not a db field - high level view of the relationship between users and posts
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')

    # repr method tell python how to print objs of this class
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    # password hash logic
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    # indexed to retrieve posts chronologically
    # default func sets field to the value returned by the func
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    # not all dbs create an index for fkeys
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)