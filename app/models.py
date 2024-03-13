from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
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
    
class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    # indexed to retrieve posts chronologically
    # default func sets field to the value returned by the func
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    # not all dbs create an index for fkeys
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeginKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)