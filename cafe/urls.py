from django.urls import path

from cafe.views import (
    index,
toggle_assign_to_dish,
    DishTypeListView,
    IngredientListView,
    DishListView,
    DishDetailView,
    CookListView,
    CookDetailView,
)

urlpatterns = [
    path("", index, name="index"),
    path("dishtypes/", DishTypeListView.as_view(), name="dish-type-list"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dishes/<int:pk>/toggle-assign/",
         toggle_assign_to_dish, name="toggle-dish-assign",),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    path("cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
]

app_name = "cafe"
