from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import RedirectView

from courses.models import Enrollment


def home(request):
    return render(request, 'main/home.html')


def about(request):
    return render(request, 'main/about.html')


def contact(request):
    return render(request, 'main/contact.html')


def faq(request):
    return render(request, 'main/faq.html')


@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'main/dashboard.html', {'enrollments': enrollments})


class InstructorDashboardRedirect(RedirectView):
    permanent = False
    pattern_name = 'course_list'
