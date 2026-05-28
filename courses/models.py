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

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
    


class Note(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    file = models.FileField(
        upload_to='course_notes/'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

