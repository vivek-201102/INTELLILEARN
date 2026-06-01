
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from courses.models import Course, Instructor, Enrollment


def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def faq(request):
    return render(request, 'main/faq.html')

def contact(request):
    return render(request, 'main/contact.html')

def course(request):
    return render(request, 'main/courses.html')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'main/dashboard.html')




@login_required
def my_courses(request):

    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course')

    return render(request, 'main/my_courses.html', {
        'enrollments': enrollments
    })


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def instructor_dashboard(request):

    try:
        # Get Logged-in Instructor
        instructor = Instructor.objects.get(user=request.user)

    except Instructor.DoesNotExist:

        messages.error(
            request,
            "Instructor profile not found."
        )

        return redirect('institute_login')

    # Get All Courses of Instructor
    courses = Course.objects.filter(
        instructor=instructor
    )

    # Total Courses
    total_courses = courses.count()

    # Total Unique Students
    total_students = User.objects.filter(
        enrollment__course__in=courses
    ).distinct().count()

    # Dummy Rating
    rating = 4.8

    context = {
        'instructor': instructor,
        'courses': courses,
        'total_courses': total_courses,
        'total_students': total_students,
        'rating': rating,
    }

    return render(
        request,
        'main/instructor_dashboard.html',
        context
    )





@login_required
def instructor_courses(request):

    try:
        instructor = Instructor.objects.get(user=request.user)

    except Instructor.DoesNotExist:
        return redirect('institute_login')

    # Get courses assigned to instructor
    courses = Course.objects.filter(instructor=instructor)

    context = {
        'instructor': instructor, 
        'courses': courses,

    }

    return render(request, 'main/instructor_courses.html', context)