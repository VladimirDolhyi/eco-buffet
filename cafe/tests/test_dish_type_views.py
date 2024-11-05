from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cafe.models import DishType

DISH_TYPE_URL = reverse("cafe:dish-type-list")


class PublicDishTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_TYPE_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_dish_types(self):
        DishType.objects.create(name="Drinks")
        DishType.objects.create(name="Salads")
        response = self.client.get(DISH_TYPE_URL)
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]), list(dish_types)
        )
        self.assertTemplateUsed(response, "cafe/dish_type_list.html")


class DishTypeNameSearchTest(TestCase):
    def setUp(self):
        self.dish_type1 = DishType.objects.create(name="Drinks")
        self.dish_type2 = DishType.objects.create(name="Salads")
        self.dish_type3 = DishType.objects.create(name="Soups")

        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(username="test", password="test123")

    def test_search_by_name(self):
        response = self.client.get(reverse(
            "cafe:dish-type-list"), {"name": "Drinks"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Drinks")
        self.assertNotContains(response, "Salads")
        self.assertNotContains(response, "Soups")

    def test_search_no_results(self):
        response = self.client.get(
            reverse("cafe:dish-type-list"), {"name": "Desserts"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "There are no dish types in the cafe."
        )

    def test_search_partial_name(self):
        response = self.client.get(reverse(
            "cafe:dish-type-list"), {"name": "Drin"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Drinks")
        self.assertNotContains(response, "Salads")
        self.assertNotContains(response, "Soups")

    def test_empty_search(self):
        response = self.client.get(
            reverse("cafe:dish-type-list"), {"name": ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Drinks")
        self.assertContains(response, "Salads")
        self.assertContains(response, "Soups")
