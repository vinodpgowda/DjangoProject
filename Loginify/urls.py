from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("signup/", views.signup),
    path("login/", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("users/", views.get_all_users),
    path("users/<str:username>/", views.user_detail_by_id),
    path("users/email/<str:email>/", views.user_detail_by_email),
]
