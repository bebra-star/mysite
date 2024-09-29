from django.urls import include, path

from main.views import page_not_found

urlpatterns = [
    path("", include("main.urls")),
    path("registration1", include("main.urls")),
    path("mine", include("main.urls")),
    path("login", include("main.urls")),  # подключаем urls из приложения main
]

handler404 = page_not_found
