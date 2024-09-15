from django.urls import path


from .views import *

# html page views
urlpatterns = [
    path("", render_main),
    path("dict/<int:id>", render_dictionary),
]

# api endpoints
urlpatterns += [
    path("api/register", register),
    path("api/dictionary", dictionary),
    path("api/dictionary/<int:id>", get_dictionary_by_id),
]