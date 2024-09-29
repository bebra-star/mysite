from django.urls import path


from .views import *

# html page views
urlpatterns = [
    path("", render_main, name="main"),
    path("registration", render_register),
    path("mine", mine),
    path("login", render_login),
    # <int:id> - переменная id, передается параметром в функцию render_dictionary
    path("dict/<int:id>", render_dictionary),
    path("user/<int:id>", render_user),
    path("profile", render_profile),
]

# api endpoints
urlpatterns += [
    path("api/register", handle_register),
    path("api/dictionary", handle_create_dictionary),
    path("api/login", handle_login),
    path("api/logout", handle_logout),
]
