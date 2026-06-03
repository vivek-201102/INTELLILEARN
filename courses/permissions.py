from accounts.models import Institute
from courses.models import Instructor


def user_can_manage_course(user, course):
    """
    Institute users may manage courses belonging to their institute.
    Instructors may manage only courses where they are the assigned instructor.
    """
    if not user.is_authenticated:
        return False

    institute = Institute.objects.filter(user=user).first()
    if institute and course.institute_id == institute.id:
        return True

    instructor = Instructor.objects.filter(user=user).first()
    if instructor and course.instructor_id == instructor.id:
        return True

    return False


def course_manage_denied_response(request, course):
    """Return a redirect response if the user cannot manage this course."""
    from django.contrib import messages
    from django.shortcuts import redirect

    if user_can_manage_course(request.user, course):
        return None

    messages.error(
        request,
        "You can only add or edit notes and quizzes for courses assigned to you."
    )
    return redirect('course_detail', pk=course.pk)
