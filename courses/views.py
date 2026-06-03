from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from .models import Instructor, Course, Enrollment, Note
from .forms import InstructorForm, CourseForm
from django.contrib.auth.decorators import login_required
from accounts.models import Institute
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from main.utils import paginate, get_search_term, list_page_context
from .permissions import user_can_manage_course, course_manage_denied_response


def instructor_list(request):
    queryset = Instructor.objects.all().order_by('name')
    q = get_search_term(request)
    if q:
        queryset = queryset.filter(
            Q(name__icontains=q)
            | Q(qualification__icontains=q)
            | Q(experience__icontains=q)
            | Q(bio__icontains=q)
        )
    page_obj = paginate(request, queryset, per_page=8)
    context = list_page_context(request, page_obj, 'Search instructors by name or qualification…')
    return render(request, 'courses/list.html', context)

def instructor_detail(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    return render(request, 'courses/detail.html', {'instructor': instructor})

def instructor_create(request):
    if request.method == "POST":
        form = InstructorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('instructor_list')
    else:
        form = InstructorForm()
    return render(request, 'courses/form.html', {'form': form, 'title': 'Add Instructor'})

def instructor_edit(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    if request.method == "POST":
        form = InstructorForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            form.save()
            return redirect('instructor_list')
    else:
        form = InstructorForm(instance=instructor)
    return render(request, 'courses/form.html', {'form': form, 'title': 'Edit Instructor'})

def instructor_delete(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    if request.method == "POST":
        instructor.delete()
        return redirect('instructor_list')
    return render(request, 'courses/confirm_delete.html', {'instructor': instructor})

def course_list(request):
    queryset = Course.objects.select_related('instructor').order_by('-created_at')
    q = get_search_term(request)
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(instructor__name__icontains=q)
            | Q(duration__icontains=q)
        )
    page_obj = paginate(request, queryset, per_page=9)
    context = list_page_context(request, page_obj, 'Search courses by title, topic, or instructor…')
    return render(request, 'courses/courses_list.html', context)

def course_detail(request, pk):

    course = get_object_or_404(Course, pk=pk)

    is_enrolled = False

    if request.user.is_authenticated:

        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists()

    notes = course.notes.all()
    quizzes = course.quizzes.prefetch_related('questions').all()

    can_manage_course = user_can_manage_course(request.user, course)

    return render(request, 'courses/courses_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'notes': notes,
        'quizzes': quizzes,
        'can_manage_course': can_manage_course,
    })
        

def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():

            course = form.save(commit=False)
            course.institute = request.user.institute
            course.is_active = True

            course.save()

            print("Saved Course ID:", course.id)
            print("Saved Course:", course.title)

            return redirect('course_list')

        else:
            print(form.errors)

    else:
        form = CourseForm()

    return render(request, 'courses/add_courses.html', {
        'form': form,
        'title': 'Create New Course'
    })

def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            course = form.save(commit=False)

            course.institute = request.user.institute

            course.is_active = True

            course.save()

            return redirect('course_list')

    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/add_courses.html', {'form': form, 'title': 'Edit Course'})

def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/confirm_delete.html', {'course': course})





@login_required
def courses_enroll(request, pk):

    course = get_object_or_404(Course, pk=pk)
    
    already_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).exists()
   
    if not already_enrolled:
        Enrollment.objects.create(
            student=request.user,
            course=course
        )
        

    return redirect('course_detail', pk=pk)



@login_required
def institute_students(request):

    institute = request.user.institute

    queryset = Enrollment.objects.filter(
        course__institute=institute
    ).select_related(
        'student',
        'course'
    ).order_by('-enrolled_at')

    q = get_search_term(request)
    if q:
        queryset = queryset.filter(
            Q(student__username__icontains=q)
            | Q(student__email__icontains=q)
            | Q(course__title__icontains=q)
        )
    page_obj = paginate(request, queryset, per_page=15)
    context = list_page_context(request, page_obj, 'Search by student, email, or course…')
    return render(request, 'courses/institute_students.html', context)


@login_required
def course_students(request, pk):

    course = get_object_or_404(Course, pk=pk)

    queryset = Enrollment.objects.filter(
        course=course
    ).select_related('student').order_by('-enrolled_at')

    q = get_search_term(request)
    if q:
        queryset = queryset.filter(
            Q(student__username__icontains=q)
            | Q(student__email__icontains=q)
        )
    page_obj = paginate(request, queryset, per_page=12)
    context = list_page_context(request, page_obj, 'Search students by name or email…')
    context['course'] = course
    context['total_students'] = Enrollment.objects.filter(course=course).count()
    return render(request, 'courses/course_students.html', context)


def instructor_create(request):

    if request.method == "POST":

        form = InstructorForm(request.POST, request.FILES)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            instructor = form.save(commit=False)

            instructor.user = user

            instructor.save()

            return redirect('instructor_list')

    else:

        form = InstructorForm()

    return render(
        request,
        'courses/form.html',
        {
            'form': form,
            'title': 'Add Instructor'
        }
    )



    if request.method == "POST":
        username_val = request.POST.get('username')
        password_val = request.POST.get('password')
        
        user = authenticate(request, username=username_val, password=password_val)
        
        if user is not None:
            login(request, user)
            
            # --- ROLE ROUTING DETECTOR ---
            # Check 1: Is this user an Institute?
            try:
                if user.institute:
                    # Redirects to the Institute's view (your course list or equivalent management page)
                    return redirect('course_list') 
            except AttributeError:
                pass  # Not an institute, check instructor status next
            
            # Check 2: Is this user an Instructor?
            if hasattr(user, 'instructor'):
                # Redirects to the Instructor's active layout view
                return redirect('instructor_list')
                
            # Default Fallback (e.g., standard students or superusers)
            return redirect('course_list')
        else:
            messages.error(request, "Invalid authentication credentials. Please try again.")
            
    return render(request, 'courses/login.html')


    

@login_required
def manage_note(request, course_pk, note_pk=None):

    course = get_object_or_404(Course, pk=course_pk)

    denied = course_manage_denied_response(request, course)
    if denied:
        return denied

    # Edit Mode
    if note_pk:

        note = get_object_or_404(Note, pk=note_pk, course=course)

    # Add Mode
    else:

        note = None

    if request.method == "POST":

        title = request.POST.get('title')
        description = request.POST.get('description')
        file = request.FILES.get('file')

        # Edit Note
        if note:

            note.title = title
            note.description = description

            # Update file only if new file uploaded
            if file:
                note.file = file

            note.save()

            messages.success(
                request,
                "Note updated successfully."
            )

        # Add Note
        else:

            Note.objects.create(
                course=course,
                title=title,
                description=description,
                file=file
            )

            messages.success(
                request,
                "Note added successfully."
            )

        return redirect(
            reverse('course_detail', kwargs={'pk': course.pk}) + '?tab=notes'
        )

    return render(
        request,
        'courses/manage_note.html',
        {
            'course': course,
            'note': note,
            'is_edit': note is not None,
        }
    )


@login_required
def delete_note(request, course_pk, note_pk):

    course = get_object_or_404(Course, pk=course_pk)
    note = get_object_or_404(Note, pk=note_pk, course=course)

    denied = course_manage_denied_response(request, course)
    if denied:
        return denied

    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully.')
        return redirect(
            reverse('course_detail', kwargs={'pk': course.pk}) + '?tab=notes'
        )

    return render(
        request,
        'courses/delete_note.html',
        {
            'course': course,
            'note': note,
        }
    )

    # note = get_object_or_404(Note, pk=pk)

    # # Only Institute or Instructor Can Edit
    # if not (
    #     Institute.objects.filter(user=request.user).exists() or
    #     Instructor.objects.filter(user=request.user).exists()
    # ):

    #     messages.error(
    #         request,
    #         "You are not allowed to edit notes."
    #     )

    #     return redirect('course_detail', pk=note.course.pk)

    # if request.method == "POST":

    #     form = NotesForm(
    #         request.POST,
    #         request.FILES,
    #         instance=note
    #     )

    #     if form.is_valid():

    #         form.save()

    #         messages.success(
    #             request,
    #             "Note updated successfully."
    #         )

    #         return redirect(
    #             'course_detail',
    #             pk=note.course.pk
    #         )

    # else:

    #     form = NotesForm(instance=note)

    # return render(
    #     request,
    #     'courses/edit_note.html',
    #     {
    #         'form': form,
    #         'note': note
    #     }
    # )