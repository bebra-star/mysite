from django.urls import include, path

from main.render import page_not_found

urlpatterns = [
    path("", include("main.urls")),  # подключаем urls из приложения main
]

handler404 = page_not_found
