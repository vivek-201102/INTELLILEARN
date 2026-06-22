from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from accounts.models import Institute
from courses.models import Instructor


# --- Role lookup helpers -------------------------------------------------

def get_institute(user):
    """Return the Institute owned by this user, or None."""
    if not getattr(user, 'is_authenticated', False):
        return None
    return Institute.objects.filter(user=user).first()


def get_instructor(user):
    """Return the Instructor profile for this user, or None."""
    if not getattr(user, 'is_authenticated', False):
        return None
    return Instructor.objects.filter(user=user).first()


# --- Course-level authorization -----------------------------------------

def user_can_manage_course(user, course):
    """
    Institute users may manage courses belonging to their institute.
    Instructors may manage only courses where they are the assigned instructor.
    """
    if not getattr(user, 'is_authenticated', False):
        return False

    institute = get_institute(user)
    if institute and course.institute_id == institute.id:
        return True

    instructor = get_instructor(user)
    if instructor and course.instructor_id == instructor.id:
        return True

    return False


def course_manage_denied_response(request, course):
    """Return a redirect response if the user cannot manage this course."""
    if user_can_manage_course(request.user, course):
        return None

    messages.error(
        request,
        "You can only add or edit notes and quizzes for courses assigned to you."
    )
    return redirect('course_detail', pk=course.pk)


# --- Role-gating decorators ----------------------------------------------

def institute_required(view_func):
    """Allow only logged-in users who own an Institute."""
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        institute = get_institute(request.user)
        if institute is None:
            messages.error(request, "Only institute accounts can access that page.")
            return redirect('institute_login_view')
        request.institute = institute
        return view_func(request, *args, **kwargs)
    return _wrapped


def instructor_required(view_func):
    """Allow only logged-in users who have an Instructor profile."""
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        instructor = get_instructor(request.user)
        if instructor is None:
            messages.error(request, "Only instructor accounts can access that page.")
            return redirect('institute_login_view')
        request.instructor = instructor
        return view_func(request, *args, **kwargs)
    return _wrapped
