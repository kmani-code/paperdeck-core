from django.urls import path
from questions.controller.questioncontroller import question, generate_questions

urlpatterns = [
    path('', question),
    path('generate/', generate_questions),
]
