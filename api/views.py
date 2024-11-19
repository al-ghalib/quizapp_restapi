from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer


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