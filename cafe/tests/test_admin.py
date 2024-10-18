from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testadmin",
        )
        self.client.force_login(self.admin_user)
        self.cook = get_user_model().objects.create_user(
            username="cook",
            password="testcook",
            years_of_experience=3,
        )

    def test_cook_years_of_experience_listed(self):
        """
        Test that a cook's years of experience is in list_display on cook admin page.
        :return:
        """
        url = reverse("admin:cafe_cook_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)

    def test_cook_detail_years_of_experience_listed(self):
        """
        Test that a cook's years of experience is on cook detail admin page.
        :return:
        """
        url = reverse("admin:cafe_cook_change", args=[self.cook.id])
        res = self.client.get(url)
        self.assertContains(res, self.cook.years_of_experience)

    def test_cook_add_years_of_experience_listed(self):
        """
        Test that a cook's years of experience is on cook add admin page.
        :return:
        """
        url = reverse("admin:cafe_cook_add")
        res = self.client.get(url)
        self.assertContains(res, "Years of experience")
