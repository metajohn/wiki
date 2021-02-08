from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("new", views.new, name="new"),
    path("random", views.random_entry, name="random")
]
