import json
import logging

import bcrypt
from django.db import IntegrityError
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from Fridgify_Backend.models import Users, UserSerializer
from Fridgify_Backend.models import exceptions
from Fridgify_Backend.utils import api_utils
from Fridgify_Backend.utils.decorators import check_body


logger = logging.getLogger(__name__)
unique_keys = ("username", "password", "email", "name", "surname", "birth_date")


@swagger_auto_schema(
    method="post",
    operation_description="Create a new user",
    request_body=UserSerializer,
    responses={
        201: openapi.Response("Created user", openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "name": openapi.Schema(type=openapi.TYPE_STRING),
                "surname": openapi.Schema(type=openapi.TYPE_STRING),
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "birth_date": openapi.Schema(type=openapi.TYPE_STRING, pattern="YYYY-mm-dd"),
            }
        )),
        409: "User already exists. Body contains duplicate keys",
    },
    security=[]
)
@api_view(["POST"])
@check_body(*unique_keys)
def register_view(request):
    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        logger.error(f"Couldn't parse JSON:\n {request.body.decode('utf-8')}")
        raise ParseError()
    logger.info(f"Register a new user ({body['username']})")
    try:
        logger.info("Create encrypted password...")
        password = bcrypt.hashpw(body["password"].encode("utf-8"), bcrypt.gensalt())
        logger.info("Create new user...")
        obj, created = Users.objects.get_or_create(
            username=body["username"],
            password=password.decode("utf-8"),
            email=body["email"],
            name=body["name"],
            surname=body["surname"],
            birth_date=body["birth_date"],
        )
        if created:
            logger.info("Created...")
            return Response(data=UserSerializer(obj).data, status=201)
        else:
            duplicate_keys = api_utils.non_unique_keys(body, Users, *unique_keys)
            logger.error(f"Object was not created for {','.join(duplicate_keys)}. No Integrity Error thrown.")
            raise exceptions.ConflictException(detail=f"{' and '.join(duplicate_keys)} already exist(s)")
    except IntegrityError:
        duplicate_keys = api_utils.non_unique_keys(body, Users, *unique_keys)
        logger.error(f"Integrity Error for {','.join(duplicate_keys)}")
        raise exceptions.ConflictException(detail=f"{' and '.join(duplicate_keys)} already exist(s)")
