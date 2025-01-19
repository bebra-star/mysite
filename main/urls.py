from django.urls import path

from main.middleware import auth_mw, dict_mw, test_mw

from .render import *
from .handler import *

# html page views
urlpatterns = [
    path("", render_main, name="main"),
    path("registration", render_register),
    path("my-dicts", render_my_dicts),
    path("login", render_login),
    # <int:id> - переменная id, передается параметром в функцию render_dictionary
    path("dict/<int:dict_id>", render_dictionary),
    path("dict/<int:dict_id>/test", render_test),
    path("user/<int:user_id>", render_user),
    path("profile", render_profile),
    path("create-dict", render_create_dict),
]

# api endpoints
urlpatterns += [
    path("api/register", handle_register),
    path("api/login", handle_login),
    path("api/logout", auth_mw(handle_logout)),
    path("api/dictionary", auth_mw(handle_create_dictionary)),
    path("api/start-test", auth_mw(handle_start_test)),
    path(
        "api/dictionary/<int:dict_id>/test/word",
        auth_mw(dict_mw(test_mw(handle_get_test_word))),
    ),
    path(
        "api/dictionary/<int:dict_id>/test/answer-word",
        auth_mw(dict_mw(test_mw(handle_answer_test_word))),
    ),
    path(
        "api/dictionary/<int:dict_id>/test/skip-word",
        auth_mw(dict_mw(test_mw(handle_skip_test_word))),
    ),
    path(
        "api/dictionary/<int:dict_id>/test/i-know-word",
        auth_mw(dict_mw(test_mw(handle_i_know_test_word))),
    ),
    path("api/dictionary/<int:dict_id>", auth_mw(dict_mw(handle_get_dictionary))),
]
