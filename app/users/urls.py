from django.urls import path

from users.views import index, avatar, password

app_name = "users"

urlpatterns = [
    path("", index),
    path("avatar/", avatar),
    path("password/", password),
]
