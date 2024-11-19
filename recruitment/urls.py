from django.urls import path
from . import views

app_name = "recruitment"
urlpatterns = [
    path("", views.index, name="index"),
    path("details/<int:job_id>", views.details, name="details"),
    path("search", views.search, name="search"),
    path("generate", views.generate, name="generate"),
]