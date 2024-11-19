from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('questions/', get_questions, name='get_questions'),
    path('questions/<int:question_id>/', get_question_details, name='get_question_details'),
    path('questions/create', create_question, name='create_question'),
]
