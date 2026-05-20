from django.urls import path
from users.controller.usercontroller import register, login, refresh_token, me, update_profile, change_password, invite_user, list_org_users

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('refresh/', refresh_token),
    path('me/', me),
    path('profile/', update_profile),
    path('change-password/', change_password),
    path('invite/', invite_user),
    path('org-users/', list_org_users),
]
