from django.urls import include, path
from django.http import HttpResponse

from main.views import page_not_found

urlpatterns = [
    path("", include("main.urls")),
]

handler404 = page_not_found
