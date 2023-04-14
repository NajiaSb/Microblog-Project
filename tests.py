#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest

import onetimepass

from app import create_app, db
from app.models import User, Post
from config import Config
from app.auth.forms import LoginForm


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # adding the following for testing methods
        self.user = User(username='test_user', email='test_user@example.com')
        self.user.password = 'password'
        self.user.token = 'test_token'
        self.user.token_expiration = datetime.utcnow() + timedelta(minutes=5)
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='tester')
        u.password = 'Password123!'
        self.assertFalse(u.verify_password('Password1234!'))
        self.assertTrue(u.verify_password('Password123!'))

    def test_get_totp_uri(self):
        totp_uri = self.user.get_totp_uri()
        self.assertIn('otpauth://totp/2FA-Demo:test_user', totp_uri)
        self.assertIn('secret={}'.format(self.user.otp_secret), totp_uri)
        self.assertIn('issuer=2FA-Demo', totp_uri)

    def test_verify_totp(self):
        valid_token = onetimepass.get_totp(self.user.otp_secret)
        invalid_token = '123456'
        self.assertTrue(self.user.verify_totp(valid_token))
        self.assertFalse(self.user.verify_totp(invalid_token))

    def test_get_reset_password_token(self):
        u = User(username='tester', email='tester@gmail.com')
        db.session.add(u)
        db.session.commit()
        token = u.get_reset_password_token()
        self.assertIsNotNone(token)

    def test_verify_reset_password_token(self):
        u = User(username='tester', email='tester@example.com')
        db.session.add(u)
        db.session.commit()
        token = u.get_reset_password_token()
        self.assertIsNotNone(token)
        user = User.verify_reset_password_token(token)
        self.assertIsNotNone(user)
        self.assertEqual(u.id, user.id)

    # def test_avatar(self):
    #     u = User(username='john', email='john@example.com')
    #     self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
    #                                      'd4c74594d841139328695756648b6bd6'
    #                                      '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
