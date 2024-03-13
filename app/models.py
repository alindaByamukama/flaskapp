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
    # repr method tell python how to print objs of this class
    def __repr__(self):
        return '<User {}>'.format(self.username)