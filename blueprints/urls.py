from django.urls import path
from blueprints.controller.blueprintcontroller import blueprint

urlpatterns = [
    path('', blueprint),
]
