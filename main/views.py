from django.db import IntegrityError
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
import json
from django.shortcuts import get_object_or_404

from main.models import User, Dictionary


def render_main(request):
    context = {"dicts": Dictionary.objects.all()}
    return render(request, "main.html", context=context)


def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except ValueError:
            return JsonResponse({"error": "json validtion error"})

        try:
            User.objects.create(
                username=data.get("name"), password=data.get("password")
            )
        except IntegrityError as e:
            return JsonResponse({"error": str(e)}, status=409)

        return JsonResponse(
            {"data": "success"},
            status=201,
        )
    return JsonResponse({"error": "wrong method"}, status=405)


def render_dictionary(request, id):
    # dict = Dictionary.objects.get(id=id).first()
    # dict = Dictionary.objects.filter(id=id).first()
    dict = get_object_or_404(Dictionary, id=id)
    return render(request, "dictionary.html", context={"dict": model_to_dict(dict)})


def dictionary(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode())
        except ValueError:
            return JsonResponse({"error": "json validtion error"})

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


def get_dictionary_by_id(request, id):
    if request.method == "GET":
        try:
            obj = Dictionary.objects.get(id=id)
        except IntegrityError as e:
            return JsonResponse({"error": str(e)}, status=409)

        return JsonResponse(
            {"data": model_to_dict(obj)},
            status=201,
        )
    return JsonResponse({"error": "wrong method"}, status=405)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Нюхай бебру!</h1>")
