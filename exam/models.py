from django.db import models
from courses.models import Course

# Create your models here

class Quiz(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )

    title = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.title



class Question(models.Model):

    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question = models.TextField()

    option1 = models.CharField(max_length=255)

    option2 = models.CharField(max_length=255)

    option3 = models.CharField(max_length=255)

    option4 = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=255
    )

    def __str__(self):

        return self.question