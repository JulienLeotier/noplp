"""
    Test.py
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


class UsersManagersTests(TestCase):
    """
        Test
    """

    def test_create_user(self):
        """
            test create user
        """
        model_user = get_user_model()
        user = model_user.objects.create_user(email='normal@user.com',
                                              password='foo', tel='0646883007',
                                              pseudo='toto')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertEqual(user.tel, '0646883007')
        self.assertEqual(user.pseudo, 'toto')

        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            model_user.objects.create_user()
        with self.assertRaises(TypeError):
            model_user.objects.create_user(email='')
        with self.assertRaises(ValueError):
            model_user.objects.create_user(email='', password="foo")

    def test_create_superuser(self):
        """
            Test create super
        """
        model_user = get_user_model()
        admin_user = model_user.objects.create_superuser(
            'super@user.com', 'foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertEqual(admin_user.tel, '0646883007')
        self.assertEqual(admin_user.pseudo, 'Admin')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            model_user.objects.create_superuser(
                email='super@user.com', password='foo', is_superuser=False)
