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

# auxiliary table for followers
followers = sa.Table(
    # table name
    'followers',
    # where sql alchmey stores info on all db tables
    db.metadata,
    # pair of combined foreign keys -> a compound primary key
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('user.id'),
              primary_key=True)
)

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    # the optional helper from python allows for a col to be empty or nullable
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    # not a db field - high level view of the relationship between users and posts
    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    
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

    # many to many followers relationship
    following: so.WriteOnlyMapped['User'] = so.relationship(
        # secondary configures the association table
        secondary=followers, 
        # primaryjoin indicates the condition that links the entity to the assoc table
        primaryjoin=(followers.c.follower_id == id),
        # secondaryjoin indicates the condition that links the assoc table to the user
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers'
    )
    followers: so.WriteOnlyMapped['User'] = so.relationship(
        secondary=followers, 
        primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following'
    )

    def follow(self, user):
        if self.is_following(user):
            self.following.add(user)

    
    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)
            
    def is_following(self, user):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)
    
    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)
        
    def following_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)
    
    def following_posts(self):
        # creates refs to users as authors and as followers
        Author = so.aliased(User)
        Follower = so.aliased(User)
        return (
            # defines the entity that needs to be obtained
            sa.select(Post)
            # join the entries in the post table with the Post.author relationship
            # of_type - refer to right side of entity w/ Author or Follower alias
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), 
            # preserves entries that have no match           
                  isouter=True)
            # filter the posts by users followed by current user
            .where(Follower.id == self.id)
            # sort the results by post timestamp field in descending order
            .order_by(Post.timestamp.desc())
        )

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