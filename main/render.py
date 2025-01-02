from django.http import HttpResponseNotFound
from django.shortcuts import render

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


def render_test(request, dict_id):
    if not request.user.is_authenticated:
        return render_login(request)

    dict = Dictionary.objects.filter(id=dict_id).first()
    if not dict:
        return render(request, "404.html")

    test_session = TestSession.objects.filter(
        dictionary_id=dict_id, user_id=request.user
    ).first()
    if not test_session:
        return render_dictionary(request, dict_id)

    context = {"dict": dict}
    return render(request, "test.html", context=context)


def render_profile(request):
    if not request.user.is_authenticated:
        return render_login(request)
    return render(request, "profile.html")


def render_register(request):
    context = {"langs": Language.objects.all()}

    return render(request, "registration.html", context=context)


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

    context = {
        "dict": dict,
        "words": words,
        "test_session_exists": test_session != None,
    }

    # if not test_session:
    #     TestSession.objects.create
    # функция model_to_dict преобразует объект в словарь
    return render(request, "dictionary.html", context=context)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Нюхай бебру!</h1>")
