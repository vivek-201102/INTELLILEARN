from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q

from bookmarks.models import Bookmark
from .models import Instructor, Course, Enrollment, Note
from .forms import InstructorForm, InstructorProfileForm, CourseForm
from django.contrib.auth.decorators import login_required
from accounts.models import Institute
from django.contrib.auth.models import User
from django.contrib import messages
from main.utils import paginate, get_search_term, list_page_context
from .permissions import (
    user_can_manage_course,
    course_manage_denied_response,
    institute_required,
    get_institute,
)





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

@institute_required
def instructor_edit(request, pk):
    # An institute may only edit instructors that belong to it.
    instructor = get_object_or_404(Instructor, pk=pk, institute=request.institute)
    if request.method == "POST":
        form = InstructorProfileForm(request.POST, request.FILES, instance=instructor)
        if form.is_valid():
            form.save()
            messages.success(request, "Instructor updated successfully.")
            return redirect('instructor_list')
    else:
        form = InstructorProfileForm(instance=instructor)
    return render(request, 'courses/form.html', {'form': form, 'title': 'Edit Instructor'})

@institute_required
def instructor_delete(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk, institute=request.institute)
    if request.method == "POST":
        instructor.delete()
        messages.success(request, "Instructor deleted successfully.")
        return redirect('instructor_list')
    return render(request, 'courses/confirm_delete.html', {'instructor': instructor})



def course_list(request):

    queryset = Course.objects.select_related(
        'instructor'
    ).order_by(
        '-created_at'
    )

    q = get_search_term(request)

    if q:
        queryset = queryset.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(instructor__name__icontains=q)
            | Q(duration__icontains=q)
        )

    # Filter Section
    filter_by = request.GET.get('filter')

    if filter_by == 'free':
        queryset = queryset.filter(
            price=0
        )

    elif filter_by == 'paid':
        queryset = queryset.filter(
            price__gt=0
        )

    elif filter_by == 'latest':
        queryset = queryset.order_by(
            '-created_at'
        )

    elif filter_by == 'oldest':
        queryset = queryset.order_by(
            'created_at'
        )

    page_obj = paginate(
        request,
        queryset,
        per_page=9
    )

    context = list_page_context(
        request,
        page_obj,
        'Search courses by title, topic, or instructor…'
    )

    return render(
        request,
        'courses/courses_list.html',
        context
    )



from bookmarks.models import Bookmark

def course_detail(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    is_enrolled = False
    is_bookmarked = False

    if request.user.is_authenticated:

        is_enrolled = Enrollment.objects.filter(
            student=request.user,
            course=course
        ).exists()

        is_bookmarked = Bookmark.objects.filter(
            student=request.user,
            course=course
        ).exists()

    notes = course.notes.all()

    quizzes = course.quizzes.prefetch_related(
        'questions'
    ).all()

    can_manage_course = user_can_manage_course(
        request.user,
        course
    )

    reviews = course.reviews.select_related(
        'student'
    ).all()

    return render(
        request,
        'courses/courses_detail.html',
        {
            'course': course,
            'is_enrolled': is_enrolled,
            'is_bookmarked': is_bookmarked,
            'notes': notes,
            'quizzes': quizzes,
            'can_manage_course': can_manage_course,
            'reviews': reviews,
        }
    )        

@institute_required
def course_create(request):
    institute = request.institute
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, institute=institute)

        if form.is_valid():
            course = form.save(commit=False)
            course.institute = institute
            course.is_active = True
            course.save()

            messages.success(request, "Course created successfully.")
            return redirect('course_list')
    else:
        form = CourseForm(institute=institute)

    return render(request, 'courses/add_courses.html', {
        'form': form,
        'title': 'Create New Course'
    })

@institute_required
def course_edit(request, pk):
    institute = request.institute
    # An institute may only edit its own courses.
    course = get_object_or_404(Course, pk=pk, institute=institute)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course, institute=institute)
        if form.is_valid():
            course = form.save(commit=False)
            course.institute = institute
            course.save()
            messages.success(request, "Course updated successfully.")
            return redirect('course_list')
    else:
        form = CourseForm(instance=course, institute=institute)
    return render(request, 'courses/add_courses.html', {'form': form, 'title': 'Edit Course'})

@institute_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, institute=request.institute)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect('course_list')
    return render(request, 'courses/confirm_delete.html', {'course': course})





@login_required
def courses_enroll(request, pk):

    course = get_object_or_404(Course, pk=pk)
    
    already_enrolled = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).exists()
   
    if already_enrolled:
        messages.info(request, "You are already enrolled in this course.")
    else:
        Enrollment.objects.create(
            student=request.user,
            course=course
        )
        messages.success(request, "Enrolled successfully.")

    return redirect('course_detail', pk=pk)



@institute_required
def institute_students(request):

    institute = request.institute

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

    # Only the owning institute or the assigned instructor may see the roster.
    if not user_can_manage_course(request.user, course):
        messages.error(request, "You do not have permission to view this course's students.")
        return redirect('course_detail', pk=pk)

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


@institute_required
def instructor_create(request):
    # Only an institute can create instructors, and the new instructor is
    # bound to that institute so other institutes never see or manage it.
    if request.method == "POST":

        form = InstructorForm(request.POST, request.FILES)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            instructor = form.save(commit=False)
            instructor.user = user
            instructor.institute = request.institute
            instructor.save()

            messages.success(request, "Instructor created successfully.")
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




@login_required
def certificate_view(request, enrollment_id):

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        student=request.user
    )

    if not enrollment.certificate_eligible:

        return render(
            request,
            'courses/certificate_not_eligible.html',
            {
                'enrollment': enrollment
            }
        )

    return render(
        request,
        'courses/certificate.html',
        {
            'enrollment': enrollment
        }
    )


from .models import Review

from django.db.models import Avg
from .models import Review


@login_required
def add_review(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if not Enrollment.objects.filter(
        student=request.user,
        course=course
    ).exists():

        messages.error(
            request,
            "You must enroll before reviewing."
        )

        return redirect(
            'course_detail',
            pk=pk
        )

    review = Review.objects.filter(
        student=request.user,
        course=course
    ).first()

    reviews = Review.objects.filter(
        course=course
    ).select_related(
        'student'
    ).order_by('-created_at')

    avg_rating = reviews.aggregate(
        Avg('rating')
    )['rating__avg']

    if request.method == "POST":

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if review:

            review.rating = rating
            review.comment = comment
            review.save()

            messages.success(
                request,
                "Review updated successfully."
            )

        else:

            Review.objects.create(
                student=request.user,
                course=course,
                rating=rating,
                comment=comment
            )

            messages.success(
                request,
                "Review submitted successfully."
            )

        return redirect(
            'add_review',
            pk=pk
        )

    return render(
        request,
        'courses/add_review.html',
        {
            'course': course,
            'review': review,
            'reviews': reviews,
            'avg_rating': avg_rating or 0,
        }
    )