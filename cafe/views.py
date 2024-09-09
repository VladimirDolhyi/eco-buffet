from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from cafe.models import Cook, Dish, DishType, Ingredient


def index(request: HttpRequest) -> HttpResponse:
    """View function for the home page of the site."""

    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1,
    }

    return render(request, "cafe/index.html", context=context)


class DishTypeListView(generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "cafe/dish_type_list.html"
    paginate_by = 5


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 5

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")
        return queryset


class IngredientListView(generic.ListView):
    model = Ingredient
    paginate_by = 5
    queryset = Ingredient.objects.prefetch_related("dishes")


class CookListView(generic.ListView):
    model = Cook
    paginate_by = 5

    def get_queryset(self):
        queryset = Cook.objects.all()
        return queryset
