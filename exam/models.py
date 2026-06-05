from django.db import models
from courses.models import Course
from django.contrib.auth.models import User

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


class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField()
    total_questions = models.IntegerField()
    # We will save the student's selections as a JSON dictionary: {"question_id": "selected_string_option"}
    user_answers = models.JSONField(default=dict) 
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.score}/{self.total_questions})"