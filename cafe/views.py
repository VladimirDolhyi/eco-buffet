from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import TemplateView

from cafe.forms import (
    CookYearUpdateForm,
    CookCreationForm,
    DishForm,
    DishTypeNameSearchForm,
    IngredientNameSearchForm,
    DishNameSearchForm,
    CookUsernameSearchForm
)
from cafe.models import Cook, Dish, DishType, Ingredient


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "cafe/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["num_cooks"] = Cook.objects.count()
        context["num_dishes"] = Dish.objects.count()
        context["num_dish_types"] = DishType.objects.count()
        context["num_ingredients"] = Ingredient.objects.count()

        num_visits = self.request.session.get("num_visits", 0)
        self.request.session["num_visits"] = num_visits + 1
        context["num_visits"] = num_visits + 1

        return context


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_type_list"
    template_name = "cafe/dish_type_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = DishTypeNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = DishType.objects.all()
        form = DishTypeNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("cafe:dish-type-list")
    template_name = "cafe/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("cafe:dish-type-list")
    template_name = "cafe/dish_type_form.html"


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("cafe:dish-type-list")
    template_name = "cafe/dish_type_confirm_delete.html"


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IngredientListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = IngredientNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        form = IngredientNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("cafe:ingredient-list")


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("cafe:ingredient-list")


class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    success_url = reverse_lazy("cafe:ingredient-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["name"] = name
        context["search_form"] = DishNameSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")
        form = DishNameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("cafe:dish-list")


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("cafe:dish-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("cafe:dish-list")


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["username"] = username
        context["search_form"] = CookUsernameSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookUsernameSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookYearUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookYearUpdateForm
    success_url = reverse_lazy("cafe:cook-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if ("from" in self.request.GET
                and self.request.GET["from"] == "cook-detail"):
            context["is_update"] = True
        else:
            context["is_update"] = False
        return context


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("")


class ToggleAssignToDishView(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        cook = Cook.objects.get(id=request.user.id)
        dish = Dish.objects.get(id=pk)

        if dish in cook.dishes.all():
            cook.dishes.remove(dish)
        else:
            cook.dishes.add(dish)

        return HttpResponseRedirect(reverse_lazy("cafe:dish-detail", args=[pk]))
