from django.db.models import Count, Case, When, IntegerField, Q
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import FridgeContent


@api_view(["GET"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
def fridge_view(request):
    content = FridgeContent.objects.values(
        "fridge_id",
        "fridge__name",
        "fridge__description",
    ).annotate(
        total=Count("item_id"),
        fresh=Count(Case(
            When(expiration_date__gt=timezone.now() + timezone.timedelta(5), then=1),
            output_field=IntegerField()
        )),
        dueSoon=Count(Case(
            When(
                Q(expiration_date__gte=timezone.now()) & Q(expiration_date__lte=timezone.now() + timezone.timedelta(5)),
                then=1
            ),
            output_field=IntegerField()
        )),
        overDue=Count(Case(
            When(expiration_date__lt=timezone.now(), then=1),
            output_field=IntegerField()
        )),
    ).filter(fridge__userfridge__user=request.user).order_by("fridge_id")

    # TODO: If we can change the structure slightly to be flat, we do not need the for loop
    payload = []
    for item in content:
        fridge_state = {
            "id": item["fridge_id"],
            "name": item["fridge__name"],
            "description": item["fridge__description"],
            "content": {
                "total": item["total"],
                "fresh": item["fresh"],
                "dueSoon": item["dueSoon"],
                "overDue": item["overDue"]
            }
        }
        payload.append(fridge_state)

    return Response(data=payload, status=200)
