from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('Technical Support', 'Technical Support'),
        ('Course Inquiry', 'Course Inquiry'),
        ('Payment Issue', 'Payment Issue'),
        ('Other', 'Other'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name