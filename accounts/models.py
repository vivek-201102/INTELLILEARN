from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(
        max_length=15
    )

    def __str__(self):

        return self.user.username



class Institute(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    institute_name = models.CharField(max_length=200)

    contact = models.CharField(max_length=15)

    email = models.EmailField(unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.institute_name