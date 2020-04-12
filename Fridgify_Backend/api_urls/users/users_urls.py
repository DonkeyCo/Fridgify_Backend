from django.urls import path

from Fridgify_Backend.views.users import users, fridge_users, users_duplicate

urlpatterns = [
    # GET
    path('', users.users_view),
    path('<int:fridge_id>/', fridge_users.fridge_users_view),
    path('duplicate/', users_duplicate.users_duplicate_view)
]
