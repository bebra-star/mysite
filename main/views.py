from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
import json
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
from django.core import serializers

# Импорт моделей из models.py
from main.models import (
    Dictionary,
    User,
    WordPair,
    Language,
    TestSession,
    TestSessionWordPair,
)


def render_login(request):
    return render(request, "login.html")


def render_profile(request):
    if request.user.is_authenticated:
        return render(request, "profile.html")
    return render_login(request)


def render_register(request):
    context = {"langs": Language.objects.all()}

    return render(request, "registration.html", context=context)


def handle_start_test(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())

        user = authenticate(
            request, username=data.get("name"), password=data.get("password")
        )
        if user is None:
            return JsonResponse(
                {"data": "success"},
                status=400,
            )
        login(request, user)

        return JsonResponse(
            {"data": "success"},
            status=201,
        )

    return JsonResponse({"error": "wrong method"}, status=405)


def handle_login(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())

        user = authenticate(
            request, username=data.get("name"), password=data.get("password")
        )
        if user is None:
            return JsonResponse(
                {"data": "success"},
                status=400,
            )
        login(request, user)

        return JsonResponse(
            {"data": "success"},
            status=201,
        )

    return JsonResponse({"error": "wrong method"}, status=405)


def handle_logout(request):
    logout(request)
    return JsonResponse({}, status=204)


def render_main(request):
    # Словарь контекста, который передается в шаблон
    context = {
        # Dictionary.objects.all() - возвращает все объекты из таблицы Dictionary
        "dicts": Dictionary.objects.all().select_related("creator"),
    }

    return render(request, "main.html", context=context)


def render_create_dict(request):
    context = {"langs": Language.objects.all()}
    return render(request, "create_dict.html", context=context)


def render_my_dicts(request):
    # Словарь контекста, который передается в шаблон
    context = {
        # Dictionary.objects.all() - возвращает все объекты из таблицы Dictionary
        "dicts": Dictionary.objects.filter(creator_id=request.user.id)
    }
    return render(request, "my_dicts.html", context=context)


def handle_register(request):
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
            user = User.objects.create_user(
                username=data.get("name"),
                password=data.get("password"),
                first_language=Language.objects.get(id=data.get("first_language")),
                second_language=Language.objects.get(id=data.get("second_language")),
            )
        except IntegrityError as e:
            # обрабатываем ошибку, если пользователь уже есть в базе. Возвращаем ошибку с кодом 409 - Conflict.
            print(e)
            return JsonResponse({"error": str(e)}, status=409)

        login(request, user)
        # Возвращаем ответ с кодом 201 - Created, см. https://developer.mozilla.org/ru/docs/Web/HTTP/Status
        return JsonResponse(
            {"data": "success"},
            status=201,
        )

    # Возвращаем ошибку, если метод запроса не POST. Статус  405 - Method Not Allowed.
    return JsonResponse({"error": "wrong method"}, status=405)


def render_user(request, user_id):
    # получаем объект Dictionary по id из базы данных, возвращаем 404 если не найдено.
    user = User.objects.filter(id=user_id).first()
    if not user:
        # TODO: рендерить красивую страницу с ошибкой 404. Пример: http://www.sberbank.ru/ru/perso
        return render(request, "404.html")

    # функция model_to_dict преобразует объект в словарь
    context = {"requested_user": user}
    return render(request, "user.html", context=context)


# параметр id - переменная, которая передается в функцию render_dictionary из обработчика урлов.
def render_dictionary(request, dict_id):
    # получаем объект Dictionary по id из базы данных, возвращаем 404 если не найдено.
    dict = Dictionary.objects.filter(id=dict_id).select_related("creator").first()
    if not dict:
        return render(request, "404.html")
    words = WordPair.objects.filter(dictionary_id=dict_id)
    test_session = TestSession.objects.filter(
        user_id=request.user.id, dictionary_id=dict_id
    ).first()

    if not test_session:
        TestSession.objects.create
    # функция model_to_dict преобразует объект в словарь
    context = {"dict": dict, "words": words}
    return render(request, "dictionary.html", context=context)


def render_testing(request):
    return render(request, "testing.html")


def handle_create_dictionary(request):
    if request.method == "POST":
        data = json.loads(request.body.decode())
        try:
            dict = Dictionary.objects.create(
                name=data.get("name"),
                language1=Language.objects.get(id=data.get("language1")),
                language2=Language.objects.get(id=data.get("language2")),
                creator=request.user,
            )
        except IntegrityError as e:
            return JsonResponse({"error": str(e)}, status=409)
        for word_pair in data.get("words"):
            WordPair.objects.create(
                word1=word_pair.get("word1"),
                word2=word_pair.get("word2"),
                dictionary=dict,
            )

        return JsonResponse(
            {"data": "success"},
            status=201,
        )

    return JsonResponse({"error": "wrong method"}, status=405)


def handle_get_dictionary(request, dict_id):
    if request.method == "GET":
        dict = (
            Dictionary.objects.filter(id=dict_id)
            .select_related("language1", "language2")
            .first()
        )
        if not dict:
            return JsonResponse(
                status=404,
            )
        dict.words = WordPair.objects.filter(dictionary_id=dict_id)

        return JsonResponse(
            {
                "data": {
                    "id": dict.id,
                    "words": list(dict.words.values()),
                    "language1": model_to_dict(dict.language1),
                    "language2": model_to_dict(dict.language2),
                },
            },
            status=200,
        )

    return JsonResponse({"error": "wrong method"}, status=405)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Нюхай бебру!</h1>")
