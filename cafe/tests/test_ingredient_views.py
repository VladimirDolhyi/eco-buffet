from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cafe.models import Ingredient

INGREDIENT_URL = reverse("cafe:ingredient-list")


class PublicIngredientTest(TestCase):
    def test_login_required(self):
        res = self.client.get(INGREDIENT_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateIngredientTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_ingredients(self):
        Ingredient.objects.create(name="Carrot")
        Ingredient.objects.create(name="Potato")
        response = self.client.get(INGREDIENT_URL)
        self.assertEqual(response.status_code, 200)
        ingredients = Ingredient.objects.all()
        self.assertEqual(
            list(response.context["ingredient_list"]), list(ingredients)
        )
        self.assertTemplateUsed(response, "cafe/ingredient_list.html")


class IngredientNameSearchTest(TestCase):
    def setUp(self):
        self.ingredient1 = Ingredient.objects.create(name="Carrot")
        self.ingredient2 = Ingredient.objects.create(name="Potato")
        self.ingredient3 = Ingredient.objects.create(name="Beetroot")

        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(username="test", password="test123")

    def test_search_by_name(self):
        response = self.client.get(reverse(
            "cafe:ingredient-list"), {"name": "Carrot"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Carrot")
        self.assertNotContains(response, "Potato")
        self.assertNotContains(response, "Beetroot")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("cafe:ingredient-list"), {"name": "Fish"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "There are no ingredients in the cafe."
        )

    def test_search_partial_name(self):
        response = self.client.get(reverse(
            "cafe:ingredient-list"), {"name": "Car"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Carrot")
        self.assertNotContains(response, "Potato")
        self.assertNotContains(response, "Beetroot")

    def test_empty_search(self):
        response = self.client.get(
            reverse("cafe:ingredient-list"), {"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Carrot")
        self.assertContains(response, "Potato")
        self.assertContains(response, "Beetroot")

    def test_pagination_with_search(self):
        for index in range(10):
            Ingredient.objects.create(name=f"Name{index}")

        response_first_page = self.client.get(
            reverse("cafe:ingredient-list"), {"name": "Name", "page": 1}
        )
        self.assertEqual(response_first_page.status_code, 200)
        for index in range(5):
            self.assertContains(response_first_page, f"Name{index}")
        for index in range(5, 10):
            self.assertNotContains(response_first_page, f"Name{index}")

        response_second_page = self.client.get(
            reverse("cafe:ingredient-list"), {"name": "name", "page": 2}
        )
        self.assertEqual(response_second_page.status_code, 200)
        for index in range(5, 10):
            self.assertContains(response_second_page, f"Name{index}")
        for index in range(5):
            self.assertNotContains(response_second_page, f"Name{index}")
