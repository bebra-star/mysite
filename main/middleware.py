from django.http import JsonResponse

from main.models import Dictionary, TestSession


def auth_mw(next):
    def middleware(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"error": "Unauthorized"},
                status=403,
            )

        return next(request, *args, **kwargs)

    return middleware


def dict_mw(next):
    def middleware(request, dict_id, *args, **kwargs):
        dict = Dictionary.objects.filter(id=dict_id).first()
        if not dict:
            return JsonResponse(
                {"error": "dict not found"},
                status=404,
            )

        return next(request, dict, *args, **kwargs)

    return middleware


def test_mw(next):
    def middleware(request, dict_id, *args, **kwargs):
        test_session = TestSession.objects.filter(
            user_id=request.user.id, dictionary_id=dict_id
        ).first()
        if not test_session:
            return JsonResponse(
                {"error": "test session not found"},
                status=400,
            )

        return next(request, test_session, *args, **kwargs)

    return middleware
