
from django import forms
from .models import Instructor, Course, Note


class InstructorForm(forms.ModelForm):

            username = forms.CharField(
                widget=forms.TextInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Username'
                })
            )

            password = forms.CharField(
                widget=forms.PasswordInput(attrs={
                    'class': 'form-control',
                    'placeholder': 'Password'
                })
            )

            class Meta:
                model = Instructor

                fields = [
                    'name',
                    'qualification',
                    'experience',
                    'profile_image',
                    'bio'
                ]

                widgets = {
                    'name': forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Full Name'
                    }),

                    'qualification': forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'e.g. PhD in Computer Science'
                    }),

                    'experience': forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'e.g. 10 Years'
                    }),

                    'profile_image': forms.FileInput(attrs={
                        'class': 'form-control'
                    }),

                    'bio': forms.Textarea(attrs={
                        'class': 'form-control',
                        'rows': 5,
                        'placeholder': 'Tell us about yourself...'
                    }),
                }
                



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'instructor': forms.Select(attrs={'class': 'form-select'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
            'what_you_will_learn': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'curriculum': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'certificate_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'target_audience': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }



class NotesForm(forms.ModelForm):

    class Meta:

        model = Note

        fields = [
            'title',
            'description',
            'file'
        ]