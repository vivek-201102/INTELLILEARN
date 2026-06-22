
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

    def clean_username(self):
        from django.contrib.auth.models import User
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("That username is already taken.")
        return username

    def clean_password(self):
        from django.contrib.auth.password_validation import validate_password
        password = self.cleaned_data['password']
        validate_password(password)
        return password




class InstructorProfileForm(forms.ModelForm):
    """Instructor self-service profile (no username/password)."""

    class Meta:
        model = Instructor
        fields = [
            'name',
            'qualification',
            'experience',
            'profile_image',
            'bio',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].required = False


class CourseForm(forms.ModelForm):

    def __init__(self, *args, institute=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Only let an institute pick from its own instructors (data isolation).
        if institute is not None:
            self.fields['instructor'].queryset = Instructor.objects.filter(
                institute=institute
            )

    class Meta:
        model = Course
        # institute and is_active are set by the view, never chosen in the form.
        exclude = ['institute', 'is_active']
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