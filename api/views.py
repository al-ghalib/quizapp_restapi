from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound


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

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_questions(request):
    # Get a list of all questions with their choices.
    questions = Question.objects.all()  
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_question_details(request, question_id):
    # Get details of a single question by its ID.
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise NotFound(detail="Question not found")

    serializer = QuestionSerializer(question)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_question(request):
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        print(request.method)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)