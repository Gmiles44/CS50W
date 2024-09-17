from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("<str:title>", views.entry, name="entry"),
    path("<str:title>/edit_entry", views.edit_entry, name="edit_entry")
]
