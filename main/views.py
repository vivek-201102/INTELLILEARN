
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from courses.models import Course, Instructor, Enrollment
from .models import ContactMessage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from courses.models import Course
from courses.models import Enrollment
from exam.models import Quiz


def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'main/about.html')

def faq(request):
    return render(request, 'main/faq.html')

def contact(request):
    return render(request, 'main/contact.html')




@login_required(login_url='login')
def dashboard(request):

    student = request.user

    enrollments = Enrollment.objects.filter(student=student)

    enrolled_courses = enrollments.count()

    

    active_courses = Enrollment.objects.filter(student=student)
    upcoming_exams = Quiz.objects.all()

    context = {
        'enrolled_courses': enrolled_courses,
        
        'active_courses': active_courses,
        'upcoming_exams': upcoming_exams,
    }

    return render(
        request,
        'main/dashboard.html',
        context
    )




@login_required
def my_courses(request):
    from django.db.models import Q
    from main.utils import paginate, get_search_term, list_page_context

    queryset = Enrollment.objects.filter(
        student=request.user
    ).select_related('course', 'course__instructor').order_by('-enrolled_at')

    q = get_search_term(request)
    if q:
        queryset = queryset.filter(
            Q(course__title__icontains=q)
            | Q(course__description__icontains=q)
            | Q(course__instructor__name__icontains=q)
        )
    page_obj = paginate(request, queryset, per_page=6)
    context = list_page_context(request, page_obj, 'Search your enrolled courses…')
    return render(request, 'main/my_courses.html', context)


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


@login_required
def instructor_profile(request):
    from courses.forms import InstructorProfileForm
    from main.instructor_utils import require_instructor

    instructor, redirect_response = require_instructor(request)
    if redirect_response:
        return redirect_response

    if request.method == 'POST':
        form = InstructorProfileForm(
            request.POST,
            request.FILES,
            instance=instructor
        )
        if form.is_valid():
            profile = form.save(commit=False)
            if 'profile_image' not in request.FILES:
                profile.profile_image = instructor.profile_image
            profile.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('instructor_profile')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = InstructorProfileForm(instance=instructor)

    return render(request, 'main/instructor_profile.html', {
        'instructor': instructor,
        'form': form,
    })


@login_required
def instructor_settings(request):
    from django.contrib.auth import update_session_auth_hash
    from main.instructor_utils import require_instructor

    instructor, redirect_response = require_instructor(request)
    if redirect_response:
        return redirect_response

    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action', 'account')

        if action == 'account':
            email = request.POST.get('email', '').strip()
            if not email:
                messages.error(request, 'Email is required.')
            elif User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, 'That email is already in use.')
            else:
                user.email = email
                user.save(update_fields=['email'])
                messages.success(request, 'Account settings saved.')

        elif action == 'password':
            current = request.POST.get('current_password', '')
            new_pass = request.POST.get('new_password', '')
            confirm = request.POST.get('confirm_password', '')

            if not user.check_password(current):
                messages.error(request, 'Current password is incorrect.')
            elif len(new_pass) < 8:
                messages.error(request, 'New password must be at least 8 characters.')
            elif new_pass != confirm:
                messages.error(request, 'New passwords do not match.')
            else:
                user.set_password(new_pass)
                user.save(update_fields=['password'])
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully.')

        return redirect('instructor_settings')

    return render(request, 'main/instructor_settings.html', {
        'instructor': instructor,
        'user': user,
    })


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )

        messages.success(
            request,
            "Your message has been sent successfully!"
        )

        return redirect('contact')

    return render(request, 'main/contact.html')




def contact_messages_list(request):
    from django.db.models import Q
    from main.utils import paginate, get_search_term, list_page_context

    queryset = ContactMessage.objects.all().order_by('-created_at')
    q = get_search_term(request)
    if q:
        queryset = queryset.filter(
            Q(full_name__icontains=q)
            | Q(email__icontains=q)
            | Q(subject__icontains=q)
            | Q(message__icontains=q)
        )
    page_obj = paginate(request, queryset, per_page=12)
    context = list_page_context(request, page_obj, 'Search messages by name, email, or subject…')
    context['total_messages'] = ContactMessage.objects.count()
    return render(request, 'main/contact_messages_list.html', context)
