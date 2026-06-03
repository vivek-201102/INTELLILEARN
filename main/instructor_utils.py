from django.contrib import messages
from django.shortcuts import redirect

from courses.models import Instructor


def get_instructor_for_user(request):
    """Return the logged-in instructor or None."""
    try:
        return Instructor.objects.get(user=request.user)
    except Instructor.DoesNotExist:
        return None


def require_instructor(request):
    """Return instructor instance, or redirect to partner login."""
    instructor = get_instructor_for_user(request)
    if instructor is None:
        messages.error(request, "Instructor profile not found.")
        return None, redirect('institute_login_view')
    return instructor, None
