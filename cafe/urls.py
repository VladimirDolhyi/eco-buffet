from django.urls import path

from cafe.views import index
from cafe.views import (
    DishTypeListView,
    IngredientListView,
    DishListView,
    CookListView,
)

urlpatterns = [
    path("", index, name="index"),
    path("dishtypes/", DishTypeListView.as_view(), name="dish-type-list"),
    path("ingredients/", IngredientListView.as_view(), name="ingredient-list"),
    path("dishes/", DishListView.as_view(), name="dish-list"),
    # path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("cooks/", CookListView.as_view(), name="cook-list"),
    # path(
    #     "cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"
    # ),
]

app_name = "cafe"
