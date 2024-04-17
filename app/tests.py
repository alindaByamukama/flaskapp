import os
os.environ['DATABASE_URL'] = 'sqlite://'

from datetime import datetime, timezone, timedelta
import unittest
from app import app, db
from app.models import User, Post