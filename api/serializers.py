from django.contrib.auth.models import User
from rest_framework import serializers
from quiz.models import Question, Choice

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        # Checking two password match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "The two password fields must match."})
        return attrs

    def create(self, validated_data):
        # Creating a new user with the validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']

    def validate_choices(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "A question must have at least two choices.")
        correct_choices = [
            choice for choice in value if choice.get('is_correct')]
        if len(correct_choices) != 1:
            raise serializers.ValidationError(
                "There must be exactly one correct choice.")
        return value

    def create(self, validated_data):
        choices_data = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)

        # Bulk create choices for the question
        choices = [
            Choice(question=question, **choice_data) for choice_data in choices_data
        ]
        Choice.objects.bulk_create(choices)

        return question