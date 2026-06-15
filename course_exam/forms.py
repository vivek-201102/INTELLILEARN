from django import forms

from .models import Exam


class ExamForm(forms.ModelForm):

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