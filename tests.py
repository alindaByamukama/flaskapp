import os
# uses an in memory sqlite db during tests
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    # setup method creates an application context and pushes it
    def setUp(self) -> None:
        self.app_context = app.app_context()
        self.app_context.push()
        # creates all db table
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='julia', email='julia@example.com')
        u.set_password('joycat')
        self.assertFalse(u.check_password('jakedog'))
        self.assertTrue(u.check_password('joycat'))

    def test_follow(self):
        u1 = User(username='jon', email='jon@example.com')
        u2 = User(username='julia', email='julia@example.com')

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        following = db.session.scalars(u1.following.select()).all()
        followers = db.session.scalars(u1.followers.select()).all()

        self.assertEqual(following, [])
        self.assertEqual(followers, [])

        u1.follow(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 1)
        self.assertEqual(u2.followers_count(), 1)

        u1_following = db.session.scalars(u1.following.select()).all()
        u2_followers = db.session.scalars(u2.followers.select()).all()

        self.assertEqual(u1_following[0].username, 'susan')
        self.assertEqual(u2_followers[0].username, 'jon')

        u1.unfollow(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)