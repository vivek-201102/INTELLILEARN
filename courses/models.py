from django.db import models
from django.contrib.auth.models import User
from accounts.models import Institute


# Instructor Model
class Instructor(models.Model):
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=200)
    experience = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='instructors/')
    bio = models.TextField()

    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)

    # The institute this instructor belongs to (data isolation between institutes).
    institute = models.ForeignKey(
        Institute,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='instructors',
    )

    def __str__(self):
        return self.name


# Course Model
class Course(models.Model):

    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Pricing
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    # Course Duration
    duration = models.CharField(max_length=100)

    duration_weeks = models.PositiveIntegerField(
    default=4
    )

    # Instructor
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE
    )

    # Thumbnail / Banner
    thumbnail = models.ImageField(
        upload_to='course_thumbnails/'
    )

    banner = models.ImageField(
        upload_to='course_banners/',
        blank=True,
        null=True
    )

    # What Students Will Learn
    what_you_will_learn = models.TextField(
        help_text="Add learning outcomes"
    )

    # Course Curriculum / Topics
    curriculum = models.TextField(
        help_text="Add syllabus or topics"
    )

    # Certificate Information
    certificate_info = models.TextField(
        blank=True,
        null=True
    )

    # Requirements / Prerequisites
    requirements = models.TextField(
        blank=True,
        null=True
    )

    # Target Audience
    target_audience = models.TextField(
        blank=True,
        null=True
    )

    # Extra Fields
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    institute = models.ForeignKey(
    Institute,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    def __str__(self):
        return self.title

#Curse Purchase

from django.contrib.auth.models import User

from django.utils import timezone

class Enrollment(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    enrolled_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('student', 'course')

    @property
    def progress(self):

        total_days = self.course.duration_weeks * 7

        if total_days <= 0:
            return 0

        days_completed = (
            timezone.now().date()
            - self.enrolled_at.date()
        ).days

        return min(
            int((days_completed / total_days) * 100),
            100
        )

    @property
    def certificate_eligible(self):
        return self.progress >= 70

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"



class Note(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    title = models.CharField(max_length=200)

    description = models.TextField(
        blank=True
    )

    file = models.FileField(
        upload_to='course_notes/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class Review(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveIntegerField()

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            'student',
            'course'
        )

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"