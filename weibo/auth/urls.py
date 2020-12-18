from django.urls import path

from . import views


urlpatterns = [
    path("weibo/login/", views.weibo_login, name="weibo-login"),
    path("weibo/complete/", views.auth_complete, name="weibo-auth"),
]
