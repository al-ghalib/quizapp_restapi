from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view


from quiz.models import Question, Choice
from .serializers import *


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        # RegisterSerializer to validate the input data and create the user
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'detail': 'User registered successfully.'
            }, status=status.HTTP_201_CREATED)

        # Return errors while validation fails
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def create_question(request):
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        print(request.method)
        if serializer.is_valid():
            # Save the new question and choices
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)