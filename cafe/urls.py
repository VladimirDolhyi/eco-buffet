from django.urls import path
from cafe.views import index

urlpatterns = [
    path("", index, name="index"),
]

app_name = "cafe"
