from django.db import IntegrityError
from django.http import JsonResponse
import json
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout

# Импорт моделей из models.py
from main.helper import get_current_word_pair, get_next_word
from main.models import (
    Dictionary,
    User,
    WordPair,
    Language,
    TestSession,
    TestSessionWordPair,
)


def handle_start_test(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse(
                {"error": "Unauthorized"},
                status=403,
            )
        data = json.loads(request.body.decode())
        dict = Dictionary.objects.filter(id=data.get("dict_id")).first()
        if not dict:
            return JsonResponse(
                {"error": "dict not found"},
                status=400,
            )

        TestSession.objects.filter(
            user_id=request.user.id, dictionary_id=dict.id
        ).delete()

        test_session = TestSession.objects.create(
            dictionary=dict,
            user=request.user,
            current_word_index=0,
            is_showing_language_first=data.get("is_showing_language_first"),
        )

        for word_pair in WordPair.objects.filter(dictionary_id=dict.id):
            TestSessionWordPair.objects.create(
                test_session=test_session, word_pair=word_pair
            )

        return JsonResponse(
            {"data": "success"},
            status=200,
        )
    return JsonResponse({"error": "wrong method"}, status=405)


def handle_get_test_word(request, test_session):
    if request.method == "GET":
        return JsonResponse(
            {"data": get_current_word_pair(test_session)},
            status=200,
        )


def handle_answer_test_word(request, test_session: TestSession):
    if request.method == "POST":
        data = json.loads(request.body.decode())

        if data.get("answer") == get_current_word_pair(test_session).get("translation"):
            success = True
        else:
            success = False

        return JsonResponse(
            {
                "data": {
                    "success": success,
                    "next_word": get_next_word(test_session),
                }
            },
            status=200,
        )


def handle_skip_test_word(request, test_session: TestSession):
    if request.method == "GET":
        return JsonResponse(
            {
                "data": {
                    "next_word": get_next_word(test_session),
                }
            },
            status=200,
        )


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


def handle_get_dictionary(request, dict):
    if request.method == "GET":
        dict.words = WordPair.objects.filter(dictionary_id=dict.id)

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
