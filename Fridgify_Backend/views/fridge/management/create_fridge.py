from django.http import JsonResponse


def entry_point(request):
    return JsonResponse({"message": "create fridge"})
