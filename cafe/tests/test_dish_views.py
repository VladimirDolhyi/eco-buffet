from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from cafe.models import Dish, DishType

DISH_URL = reverse("cafe:dish-list")


class PublicDishTest(TestCase):
    def test_login_required(self):
        dish_type = DishType.objects.create(name="Soups")
        dish = Dish.objects.create(name="Green borsch",
                                   price=60.00, dish_type=dish_type)

        res = self.client.get(DISH_URL)
        self.assertNotEqual(res.status_code, 200)
        res2 = self.client.get(reverse("cafe:dish-detail", args=[dish.pk]))
        self.assertNotEqual(res2.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123",
        )
        self.client.force_login(self.user)

    def test_retrieve_dishes(self):
        dish_type = DishType.objects.create(name="Soups")
        Dish.objects.create(name="Green borsch", price=60.00, dish_type=dish_type)
        Dish.objects.create(name="Red borsch", price=65.00, dish_type=dish_type)
        response = self.client.get(DISH_URL)
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.all()
        self.assertEqual(list(response.context["dish_list"]), list(dishes))
        self.assertTemplateUsed(response, "cafe/dish_list.html")


class DishNameSearchTest(TestCase):
    def setUp(self):
        self.dish_type1 = DishType.objects.create(name="Soups")
        self.dish_type2 = DishType.objects.create(name="Salads")

        self.dish1 = Dish.objects.create(
            name="Green borsch", price=60.00, dish_type=self.dish_type1
        )
        self.dish2 = Dish.objects.create(
            name="Red borsch", price=65.00, dish_type=self.dish_type1
        )
        self.dish3 = Dish.objects.create(
            name="Shuba salad", price=70.00, dish_type=self.dish_type2
        )

        self.user = get_user_model().objects.create_user(
            username="test",
            password="test123"
        )
        self.client.login(username="test", password="test123")

    def test_search_by_name(self):
        response = self.client.get(
            reverse("cafe:dish-list"), {"name": "Green borsch"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Green borsch")
        self.assertNotContains(response, "Red borsch")
        self.assertNotContains(response, "Shuba salad")

    def test_search_no_results(self):
        response = self.client.get(reverse(
            "cafe:dish-list"), {"name": "Olivier salad"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no dishes in the cafe.")

    def test_search_partial_name(self):
        response = self.client.get(reverse("cafe:dish-list"), {"name": "borsch"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Green borsch")
        self.assertContains(response, "Red borsch")
        self.assertNotContains(response, "Shuba salad")

    def test_empty_search(self):
        response = self.client.get(reverse("cafe:dish-list"), {"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Green borsch")
        self.assertContains(response, "Red borsch")
        self.assertContains(response, "Shuba salad")

    def test_pagination_with_search(self):
        for index in range(10):
            Dish.objects.create(name=f"Name{index}",
                                price=50.00, dish_type=self.dish_type1)

        response_first_page = self.client.get(
            reverse("cafe:dish-list"), {"name": "Name", "page": 1}
        )
        self.assertEqual(response_first_page.status_code, 200)
        for index in range(5):
            self.assertContains(response_first_page, f"Name{index}")
        for index in range(5, 10):
            self.assertNotContains(response_first_page, f"Name{index}")

        response_second_page = self.client.get(
            reverse("cafe:dish-list"), {"name": "name", "page": 2}
        )
        self.assertEqual(response_second_page.status_code, 200)
        for index in range(5, 10):
            self.assertContains(response_second_page, f"Name{index}")
        for index in range(5):
            self.assertNotContains(response_second_page, f"Name{index}")
