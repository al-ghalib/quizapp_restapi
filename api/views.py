from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound, ValidationError

from django.utils import timezone
from quiz.models import Question, Choice
from .models import PracticeHistory
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


@api_view(['POST'])
def submit_answer(request, question_id):
    # Submitting answer to check if it is correct
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    answer_id = request.data.get('answer_id')

    if not answer_id:
        raise ValidationError("Answer ID is required.")

    try:
        question = Question.objects.get(id=question_id)
        choice = Choice.objects.get(id=answer_id, question=question)
    except Question.DoesNotExist:
        raise NotFound(detail="Question not found.")
    except Choice.DoesNotExist:
        raise NotFound(
            detail="Choice not found or choice not valid for this question.")

    is_correct = choice.is_correct

    PracticeHistory.objects.create(
        user=request.user,
        question=question,
        chosen_answer=choice,
        is_correct=is_correct,
        attempted_at=timezone.now()  
    )
    response_data = {
        'question_id': question.id,
        'chosen_answer': choice.text,
        'is_correct': is_correct
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_practice_history(request):
    # Retrieve the practice history of the authenticated user
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    history = PracticeHistory.objects.filter(
        user=request.user).order_by('-attempted_at')

    serializer = PracticeHistorySerializer(history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)