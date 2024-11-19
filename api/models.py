from django.db import models
from django.contrib.auth.models import User
from quiz.models import Question, Choice

class PracticeHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_answer = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.text} - {'Correct' if self.is_correct else 'Incorrect'}"
