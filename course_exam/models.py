from django.db import models
from django.contrib.auth.models import User

from courses.models import Course


class Exam(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='exams'
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    registration_deadline = models.DateTimeField()

    start_datetime = models.DateTimeField()

    end_datetime = models.DateTimeField()

    duration_minutes = models.PositiveIntegerField()

    total_marks = models.PositiveIntegerField(default=0)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    passing_marks = models.PositiveIntegerField(
        default=40
    )

    def __str__(self):
        return self.title


from django.contrib.auth.models import User


class ExamRegistration(models.Model):

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    registered_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'exam',
            'student'
        )

    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"



class ExamQuestion(models.Model):

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_text = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_answer = models.CharField(
        max_length=1,
        choices=[
            ('A', 'Option A'),
            ('B', 'Option B'),
            ('C', 'Option C'),
            ('D', 'Option D')
        ]
    )

    marks = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return self.question_text[:50]



class ExamAttempt(models.Model):

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    score = models.PositiveIntegerField(
        default=0
    )

    total_marks = models.PositiveIntegerField(
        default=0
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    submitted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_submitted = models.BooleanField(
        default=False
    )

    passed = models.BooleanField(
        default=False
    )

    class Meta:
        unique_together = (
            'exam',
            'student'
        )
    def __str__(self):
        return f"{self.student.username} - {self.exam.title}"



class StudentAnswer(models.Model):

    attempt = models.ForeignKey(
        ExamAttempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )

    question = models.ForeignKey(
        ExamQuestion,
        on_delete=models.CASCADE
    )

    selected_answer = models.CharField(
    max_length=1,
    choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ],
    blank=True,
    null=True
    )

    class Meta:
        unique_together = (
        'attempt',
        'question'    
    )
    
    
    def __str__(self):
        return f"{self.attempt.student.username} - Q{self.question.id}"
    
    