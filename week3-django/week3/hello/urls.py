from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dave", views.dave, name="dave"),
    path("<str:name>", views.greet, name="greet")
]