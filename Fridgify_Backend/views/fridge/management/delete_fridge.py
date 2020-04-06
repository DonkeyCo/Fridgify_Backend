from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Fridgify_Backend.models.backends import APIAuthentication
from Fridgify_Backend.models import Fridges, UserFridge, FridgeSerializer
from Fridgify_Backend.utils. decorators import check_fridge_access


@swagger_auto_schema(
    method="delete",
    operation_description="Delete a fridge",
    request_body=FridgeSerializer,
    responses={
        201: "Fridge deleted"
    },
    security=[{'FridgifyAPI_Token_Auth': []}]
)
@api_view(["DELETE"])
@authentication_classes([APIAuthentication])
@permission_classes([IsAuthenticated])
@check_fridge_access()
def delete_fridge_view(request, fridge_id):
    UserFridge.objects.get(user=request.user, fridge_id=fridge_id).delete()
    if UserFridge.objects.filter(fridge_id=fridge_id).count() == 0:
        Fridges.objects.get(fridge_id=fridge_id).delete()
    return Response(data={"detail": "User was removed from fridge"}, status=201)
