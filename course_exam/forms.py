from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .models import Exam
from courses.models import Course


class ExamForm(forms.ModelForm):

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.none()
        if user is None:
            return

        institute = None
        instructor = None
        try:
            institute = user.institute
        except (AttributeError, ObjectDoesNotExist):
            pass
        try:
            instructor = user.instructor
        except (AttributeError, ObjectDoesNotExist):
            pass

        if institute or instructor:
            filters = Q()
            if institute:
                filters |= Q(institute=institute)
            if instructor:
                filters |= Q(instructor=instructor)
            self.fields['course'].queryset = Course.objects.filter(filters).distinct()
    class Meta:

        model = Exam

        fields = [
            'course',
            'title',
            'description',
            'registration_deadline',
            'start_datetime',
            'end_datetime',
            'duration_minutes',
            'is_active'
        ]

        widgets = {

            'registration_deadline':
                forms.DateTimeInput(
                    attrs={'type': 'datetime-local'}
                ),

            'start_datetime':
                forms.DateTimeInput(
                    attrs={'type': 'datetime-local'}
                ),

            'end_datetime':
                forms.DateTimeInput(
                    attrs={'type': 'datetime-local'}
                )
        }




from .models import ExamQuestion

class ExamQuestionForm(forms.ModelForm):

    class Meta:
        model = ExamQuestion

        fields = [
            'question_text',
            'option_a',
            'option_b',
            'option_c',
            'option_d',
            'correct_answer',
            'marks'
        ]