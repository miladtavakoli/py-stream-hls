from test import BaseStreamTestCase, app
from repository.user import User
from sqlalchemy import func


class UserModelTestCase(BaseStreamTestCase):

    def setUp(self):
        super(UserModelTestCase, self).setUp()
        self.valid_user_data = {
            "username": "noob",
            "email": "8590410@gmail.com",
            "password": "SamPlePassWr0d!",
            "first_name": "Milad",
            "last_name": "Tavakoli"
        }

    def test_create_user(self):
        with app.app_context():
            user = User(**self.valid_user_data)
            user.save()
            saved_user = User.query.filter(func.lower(User.username) == user.username).first()
            self.assertTrue(saved_user)
            self.assertEqual(saved_user.username, self.valid_user_data['username'])
            self.assertEqual(saved_user.email, self.valid_user_data['email'])
            self.assertEqual(saved_user.password, self.valid_user_data['password'])
            self.assertEqual(saved_user.first_name, self.valid_user_data['first_name'])
            self.assertEqual(saved_user.last_name, self.valid_user_data['last_name'])

    def test_delete_user(self):
        with app.app_context():
            User.query.filter(func.lower(User.username) == self.valid_user_data['username']).first().delete()
            saved_user = User.query.filter(func.lower(User.username) == self.valid_user_data['username']).first()
            self.assertFalse(saved_user)


