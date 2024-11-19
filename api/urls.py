from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('questions/', get_questions, name='get_questions'),
    path('questions/<int:question_id>/', get_question_details, name='get_question_details'),
    path('questions/create', create_question, name='create_question'),
    path('questions/<int:question_id>/submit_answer/', submit_answer, name='submit_answer'),
    path('practice-history/', get_practice_history, name='get_practice_history'),
]
