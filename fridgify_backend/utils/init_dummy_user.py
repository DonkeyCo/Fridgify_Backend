# pylint: skip-file

import datetime
from django.utils import timezone
from django.http import HttpResponse
from django.http import JsonResponse
from fridgify_backend.models.users import Users
from fridgify_backend.models.providers import Providers
from fridgify_backend.models.fridges import Fridges
from fridgify_backend.models.user_fridge import UserFridge
from fridgify_backend.models.fridge_content import FridgeContent
from fridgify_backend.models.stores import Stores
from fridgify_backend.models.items import Items
from fridgify_backend.utils import const


def setup_database(request):
    response_users = [
        {
            "name": "dummy_name",
            "email": "dummy@d.de",
            "password": "password"
        },
        {
            "name": "testUser",
            "email": "test@user.de",
            "password": "password"
        }
    ]
    print(request.method)
    if request.method != "OPTIONS":
        return HttpResponse(status=400, content="Nice try")
    users = create_users()
    fridge = create_fridges(users)
    fill_fridges(fridge)

    if not Providers.objects.filter().exists():
        create_providers()

    return JsonResponse(status=200, data={
        "users": response_users
    })


def fill_fridges(fridges):
    items = []
    store = Stores()
    store.name = "REWE"
    store.save()
    for i in range(0, 5):
        item = Items()
        item.name = "item No. {}".format(i)
        item.description = "sdnjanddkjandakjd"
        item.store = store
        item.save()
        items.append(item)

    for fridge in fridges:
        j = 0
        for j in range(0, 5):
            fridge_content = FridgeContent()
            fridge_content.item = items[j]
            fridge_content.fridge = fridge
            fridge_content.amount = 42
            fridge_content.created_at = timezone.now()
            fridge_content.expiration_date = timezone.now() + timezone.timedelta(days=69)
            fridge_content.unit = "t"
            fridge_content.last_updated = timezone.now()
            fridge_content.save()


def create_fridges(users):
    fridges = []
    for user in users:
        fridge = Fridges()
        fridge.name = "fridge No {}".format(user.name)
        fridge.description = "dkjandkjsanddnakjd"
        fridge.save()
        fridges.append(fridge)
    i = 0
    for i in range(0, 2):
        user_fridge = UserFridge()
        user_fridge.fridge = fridges[i]
        user_fridge.user = users[i]
        user_fridge.role = const.Constants.ROLE_OWNER
        user_fridge.save()
    return fridges


def create_providers():
    provider = Providers()
    provider.name = "Fridgify"
    provider.save()
    provider2 = Providers()
    provider2.name = "Fridgify-API"
    provider2.save()


def create_users():
    users = []
    user = Users()
    user.username = "dummy_name"
    user.name = "Dummy"
    user.surname = "Name"
    user.email = "dummy@d.de"
    # encrypted password
    user.password = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
    user.birth_date = datetime.date(2000, 10, 17)
    user.save()
    user2 = Users()
    user2.username = "testUser"
    user2.name = "Test"
    user2.surname = "User"
    user2.email = "test@user.de"
    # encrypted password = password
    user2.password = "$2b$12$1hKYhKg4AU54eyES8qjRYOjInIgObjn0JJ8SlWPOpR9MzKcseMDVS"
    user2.birth_date = datetime.date(2000, 10, 17)
    user2.save()
    users.append(user)
    users.append(user2)
    return users
