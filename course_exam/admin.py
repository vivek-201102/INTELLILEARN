from django.contrib import admin
from .models import Exam


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'course',
        'registration_deadline',
        'start_datetime'
    )

    search_fields = (
        'title',
    )