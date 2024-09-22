from tkinter import E
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
import json

# Импорт моделей из models.py
from main.models import User, Dictionary

def render_main(request):
    # Словарь контекста, который передается в шаблон
    context = {
        # Dictionary.objects.all() - возвращает все объекты из таблицы Dictionary
        "dicts": Dictionary.objects.all()
    }
    return render(request, "main.html", context=context)

def register(request):
    # Проверка того, что метод запроса POST. См. https://doka.guide/tools/http-protocol/
    if request.method == "POST":
        # парсим json из тела запроса в словарь
        data = json.loads(request.body.decode())

        """
        Пытаемся создать объект User в базе.
        Если пользователь с таким ником уже есть (просходит из-за unique=True в поле username модели User),
        то выбрасывается исключение IntegrityError
        """
        try:
            User.objects.create(
                username=data.get("name"), password=data.get("password")
            )
        except IntegrityError as e:
            # обрабатываем ошибку, если пользователь уже есть в базе. Возвращаем ошибку с кодом 409 - Conflict.
            return JsonResponse({"error": str(e)}, status=409)

        # Возвращаем ответ с кодом 201 - Created, см. https://developer.mozilla.org/ru/docs/Web/HTTP/Status
        return JsonResponse(
            {"data": "success"},
            status=201,
        )

    # Возвращаем ошибку, если метод запроса не POST. Статус  405 - Method Not Allowed.
    return JsonResponse({"error": "wrong method"}, status=405)


# параметр id - переменная, которая передается в функцию render_dictionary из обработчика урлов.
def render_dictionary(request, id):
    # получаем объект Dictionary по id из базы данных, возвращаем 404 если не найдено.
    try:
        obj = Dictionary.objects.get(id=id)
    except Dictionary.DoesNotExist:
        return HttpResponse("<h1>404</h1>")

        # TODO: рендерить красивую страницу с ошибкой 404. Пример: http://www.sberbank.ru/ru/perso
        # return render(request, "404.html")

    # функция model_to_dict преобразует объект в словарь
    context = {"dict": model_to_dict(obj)}
    return render(request, "dictionary.html", context=context)


def dictionary(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        try:
            Dictionary.objects.create(
                name=data.get("name"),
                language1=data.get("language1"),
                language2=data.get("language2"),
            )
        except IntegrityError as e:
            return JsonResponse({"error": str(e)}, status=409)

        return JsonResponse(
            {"data": "success"},
            status=201,
        )

    return JsonResponse({"error": "wrong method"}, status=405)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Нюхай бебру!</h1>")
