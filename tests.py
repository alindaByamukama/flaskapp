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