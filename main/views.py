from django.db import IntegrityError
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
import json

from main.models import User


def main(request):
    return render(request, "index.html")


def ded(request):
    return render(request, "ded.html")


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


def create_dict(request):
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


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Нюхай бебру!</h1>")
