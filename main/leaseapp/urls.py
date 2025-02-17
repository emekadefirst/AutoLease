from django.urls import path
from . import views


urlpatterns = [
    path("", views.main, name="Landing page"),
    path("home", views.home, name="Home page"),
    path("detail", views.detail, name="detail page"),
   
]
