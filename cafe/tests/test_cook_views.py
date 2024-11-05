from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cafe.models import Cook

COOK_URL = reverse("cafe:cook-list")


class PublicCookTest(TestCase):
    def test_login_required(self):
        cook = Cook.objects.create(username="Adam", years_of_experience=3)

        res = self.client.get(COOK_URL)
        self.assertNotEqual(res.status_code, 200)
        res2 = self.client.get(reverse("cafe:cook-detail", args=[cook.pk]))
        self.assertNotEqual(res2.status_code, 200)


class PrivateCookTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_cooks(self):
        Cook.objects.create(username="Adam", years_of_experience=3)
        Cook.objects.create(username="Eve", years_of_experience=2)
        response = self.client.get(COOK_URL)
        self.assertEqual(response.status_code, 200)
        cooks = Cook.objects.all()
        self.assertEqual(list(response.context["cook_list"]), list(cooks))
        self.assertTemplateUsed(response, "cafe/cook_list.html")


class CookUsernameSearchTest(TestCase):
    def setUp(self):
        self.cook1 = Cook.objects.create(username="adam", years_of_experience=3)
        self.cook2 = Cook.objects.create(username="eve", years_of_experience=2)
        self.cook3 = Cook.objects.create(username="casey_ryback", years_of_experience=1)

        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(username="test", password="test123")

    def test_search_valid_username(self):
        response = self.client.get(reverse(
            "cafe:cook-list"), {"username": "adam"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "adam")
        self.assertNotContains(response, "eve")
        self.assertNotContains(response, "casey_ryback")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("cafe:cook-list"), {"username": "Usyk"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "adam")
        self.assertNotContains(response, "eve")
        self.assertNotContains(response, "casey_ryback")

    def test_search_empty_username(self):
        response = self.client.get(reverse(
            "cafe:cook-list"), {"username": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "adam")
        self.assertContains(response, "eve")
        self.assertContains(response, "casey_ryback")

    def test_search_partial_username(self):
        response = self.client.get(reverse(
            "cafe:cook-list"), {"username": "casey"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "adam")
        self.assertNotContains(response, "eve")
        self.assertContains(response, "casey_ryback")
