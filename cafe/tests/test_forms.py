from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cafe.forms import CookCreationForm


class FormsTests(TestCase):
    def test_cook_creation_form_with_years_of_experience_first_last_name_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": 3,
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)


class PrivateCookTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_create_cook(self):
        form_data = {
            "username": "new_user",
            "password1": "user1test",
            "password2": "user1test",
            "first_name": "Test first",
            "last_name": "Test last",
            "years_of_experience": 3,
        }
        self.client.post(reverse("cafe:cook-create"), form_data)
        new_user = get_user_model().objects.get(username=form_data["username"])

        self.assertEqual(new_user.first_name, form_data["first_name"])
        self.assertEqual(new_user.last_name, form_data["last_name"])
        self.assertEqual(new_user.years_of_experience, form_data["years_of_experience"])
