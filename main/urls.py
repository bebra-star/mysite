from django.urls import path


from .views import *

# html page views
urlpatterns = [
    path("", render_main),
    # <int:id> - переменная id, передается параметром в функцию render_dictionary
    path("dict/<int:id>", render_dictionary),
]

# api endpoints
urlpatterns += [
    path("api/register", register),
    path("api/dictionary", dictionary),
]
