from urllib import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from .models import UserProfile
from django.db.models import Q
from .models import Institute
from django.contrib.auth.decorators import login_required
from courses.models import Course, Instructor, Enrollment



def registration(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password Match Check
        if password != confirm_password:

            messages.error(request, "Passwords do not match")

            return redirect('registration')

        # Username Exists
        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists")

            return redirect('registration')

        # Email Exists
        if User.objects.filter(email=email).exists():

            messages.error(request, "Email already exists")

            return redirect('registration')

        # Create User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create Profile
        UserProfile.objects.create(
            user=user,
            phone=phone
        )

        messages.success(request, "Account created successfully")

        return redirect('login')

    return render(request, 'accounts/registration.html')


def login_user(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        # Get Username Using Email
        try:

            user_obj = User.objects.get(email=email)

            username = user_obj.username

        except User.DoesNotExist:

            messages.error(request, "Invalid Email")

            return redirect('login')

        # Authenticate
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(request, "Login Successful")

            return redirect('home')

        else:

            messages.error(request, "Invalid Password")

            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')




def institute_register(request):
    if request.method == "POST":
        institute_name = request.POST.get('institute_name')
        username = request.POST.get('username')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('institute_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('institute_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('institute_register')

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create Institute profile
        Institute.objects.create(
            user=user,
            institute_name=institute_name,
            contact=contact,
            email=email
        )

        messages.success(request, "Institute Registered Successfully! Please Login.")
        return redirect('institute_login_view')

    return render(request, 'accounts/institute_register.html')

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

from accounts.models import Institute
from courses.models import Instructor


def institute_login_view(request):
    print("test")
    # Already Logged In
    if request.user.is_authenticated:
        print("test2")
        # Institute User
        if Institute.objects.filter(user=request.user).exists():
            return redirect('institute_dashboard')

        # Instructor User
        elif Instructor.objects.filter(user=request.user).exists():
            return redirect('instructor_dashboard')

    if request.method == "POST":
        print("test3")
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        print(username_or_email,password)
        user = None

        # Login using Email OR Username
        if '@' in username_or_email:

            try:
                user_obj = User.objects.get(email=username_or_email)

                user = authenticate(
                    username=user_obj.username,
                    password=password
                )

            except User.DoesNotExist:
                user = None

        else:

            user = authenticate(
                username=username_or_email,
                password=password
            )

        if user is not None:

            login(request, user)

            # Institute Redirect
            if Institute.objects.filter(user=user).exists():

                messages.success(request, "Institute Login Successful")
                return redirect('institute_dashboard')

            # Instructor Redirect
            elif Instructor.objects.filter(user=user).exists():

                messages.success(request, "Instructor Login Successful")
                return redirect('instructor_dashboard')

            else:

                logout(request)

                messages.error(
                    request,
                    "This account is not registered."
                )

        else:

            messages.error(
                request,
                "Invalid Username/Email or Password"
            )

    return render(request, 'accounts/institute_login.html')

@login_required(login_url='institute_login_view')
def institute_dashboard(request):

    try:
        institute_data = Institute.objects.get(user=request.user)

        total_instructors = Instructor.objects.count()

        total_courses = Course.objects.count()

        total_students = Enrollment.objects.values(
            'student'
        ).distinct().count()

        total_enrollments = Enrollment.objects.count()

        context = {
            'institute': institute_data,
            'total_instructors': total_instructors,
            'total_courses': total_courses,
            'total_students': total_students,
            'total_enrollments': total_enrollments,
        }

        return render(
            request,
            'accounts/institute_dashboard.html',
            context
        )

    except Institute.DoesNotExist:

        messages.error(request, "Access Denied.")

        return redirect('institute_login_view')


def institute_logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('institute_login_view')
