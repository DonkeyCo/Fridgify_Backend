import json

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import Fridges,FridgeSerializer
from Fridgify_Backend.utils.decorators import check_body, check_fridge_access


@swagger_auto_schema(
    method="patch",
    operation_description="Update fridge attributes",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "description": openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={
        200: openapi.Response("Edited fridge", FridgeSerializer),
        404: "Fridge not found",
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["PATCH"])
@check_body("fridge_id")
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_fridge_access()
def edit_fridge_view(request):
    body = json.loads(request.body)
    fridge_id = body["fridge_id"]
    update_values = {}
    for key in body.keys():
        if key in ("name", "description"):
            update_values[key] = body[key]
    Fridges.objects.filter(fridge_id=fridge_id).update(**update_values)
    try:
        fridge = Fridges.objects.get(fridge_id=fridge_id)
        return Response(data=serialize_object(fridge, True), status=200)
    except Fridges.DoesNotExist:
        raise NotFound(detail="Fridge not found")
