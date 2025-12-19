from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


class UserModelTestCase(TestCase):
    def test_create_user_with_email_and_password(self):
        """Создание юзера с мейлом и паролем"""
        user = User.objects.create_user(
            email="user@test.com",
            password="12345",
        )
        self.assertEqual(user.email, "user@test.com")
        self.assertTrue(user.check_password("12345"))

    def test_create_user_without_email(self):
        """создание юзера без мейла"""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email="",
                password="QAZplm",
            )
