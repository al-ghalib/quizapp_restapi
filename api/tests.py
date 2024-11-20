from rest_framework.test import APITestCase
from rest_framework import status
from quiz.models import Question, Choice
from django.contrib.auth.models import User


class QuestionViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')
        
        # Creating a question and its choices
        self.question = Question.objects.create(text="What is the capital of Bangladesh?")
        self.choice1 = Choice.objects.create(question=self.question, text="Dhaka", is_correct=True)
        self.choice2 = Choice.objects.create(question=self.question, text="Rajshahi", is_correct=False)
        self.choice3 = Choice.objects.create(question=self.question, text="Sylhet", is_correct=False)

        # Authenticating the user
        self.client.login(username='testuser', password='password')


    def test_get_list_of_questions(self):
        response = self.client.get('/api/v1/questions/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  
        self.assertEqual(response.data[0]['text'], self.question.text)

        choices = response.data[0]['choices']
        self.assertEqual(len(choices), 3)
        self.assertEqual(choices[0]['text'], self.choice1.text)
        self.assertTrue(choices[0]['is_correct'])
        self.assertEqual(choices[1]['text'], self.choice2.text)
        self.assertFalse(choices[1]['is_correct'])
        self.assertEqual(choices[2]['text'], self.choice3.text)
        self.assertFalse(choices[2]['is_correct'])


    def test_get_question_details(self):
        response = self.client.get(f'/api/v1/questions/{self.question.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.question.text)

        choices = response.data['choices']
        self.assertEqual(len(choices), 3)
        self.assertEqual(choices[0]['text'], self.choice1.text)


    def test_create_new_question(self):
        new_question_data = {
            'text': "What is the largest ocean on Earth?",
            'choices': [
                {'text': 'Atlantic Ocean', 'is_correct': False},
                {'text': 'Pacific Ocean', 'is_correct': True},
                {'text': 'Indian Ocean', 'is_correct': False},
            ]
        }
        response = self.client.post('/api/v1/questions/', new_question_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], new_question_data['text'])
        self.assertEqual(len(response.data['choices']), 3)


    def test_submit_answer_correct(self):
        answer_data = {'choice': self.choice1.id}
        response = self.client.post(f'/api/v1/questions/{self.question.id}/submit_answer/', answer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Answer submitted successfully!')
        self.assertTrue(response.data['is_correct'])


    def test_submit_answer_incorrect(self):
        answer_data = {'choice': self.choice2.id}
        response = self.client.post(f'/api/v1/questions/{self.question.id}/submit_answer/', answer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Answer submitted successfully!')
        self.assertFalse(response.data['is_correct'])


    def test_submit_answer_missing_choice(self):
        answer_data = {}  
        response = self.client.post(f'/api/v1/questions/{self.question.id}/submit_answer/', answer_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Answer ID is required')


    def test_create_question_less_than_two_choices(self):
        # Trying to create a question with only one choice
        new_question_data = {
            'text': "What is the largest ocean on Earth?",
            'choices': [{'text': 'Pacific Ocean', 'is_correct': True}]
        }
        response = self.client.post('/api/v1/questions/', new_question_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'A question must have at least two choices.')


    def test_create_question_multiple_correct_choices(self):
        # Trying to create a question with more than one correct choice
        new_question_data = {
            'text': "What is the largest ocean on Earth?",
            'choices': [
                {'text': 'Atlantic Ocean', 'is_correct': True},
                {'text': 'Pacific Ocean', 'is_correct': True},
                {'text': 'Indian Ocean', 'is_correct': False},
            ]
        }
        response = self.client.post('/api/v1/questions/', new_question_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'There must be exactly one correct choice.')


    def test_get_user_practice_history(self):
        # Submitting answer to record history
        answer_data = {'choice': self.choice1.id}
        self.client.post(f'/api/v1/questions/{self.question.id}/submit_answer/', answer_data, format='json')

        response = self.client.get('/api/v1/user/practice_history/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 
        self.assertEqual(response.data[0]['question']['text'], self.question.text)
