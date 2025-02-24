from django.urls import path
from . import views


urlpatterns = [
    path("", views.main, name="Landing page"),
    path("home", views.home, name="Home page"),
    path("detail/<int:id>", views.detail, name="detail page"),
    path("filter", views.vehicle_filter, name="filter"),
    path("login", views.login_view, name="login"),
    path("signup", views.signup, name="signup"),
    path('logout', views.logout_user, name="logout"),
]
