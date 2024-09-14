from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from pprint import pprint
import json


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
        if data.get("name") == "dedkov":
            return JsonResponse(
                {"error": "conflict name"},
                status=409,
            )
        return JsonResponse(
            {"data": "success"},
            status=201,
        )
    return JsonResponse({"error": "wrong method"}, status=405)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Нюхай бебру</h1>")
