from accounts.models import Institute
from courses.models import Instructor


def user_navigation(request):
    """Expose role flags for consistent nav across templates."""
    is_institute_user = False
    is_instructor_user = False
    is_student_user = False

    if request.user.is_authenticated:
        is_institute_user = Institute.objects.filter(user=request.user).exists()
        is_instructor_user = Instructor.objects.filter(user=request.user).exists()
        is_student_user = not is_institute_user and not is_instructor_user

    return {
        'is_institute_user': is_institute_user,
        'is_instructor_user': is_instructor_user,
        'is_student_user': is_student_user,
    }
