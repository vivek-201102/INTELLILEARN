from django.shortcuts import (render, redirect, get_object_or_404)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exam, ExamAttempt, ExamQuestion, ExamRegistration, StudentAnswer
from .forms import ExamForm, ExamQuestionForm
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
from courses.models import Course


def get_user_institute(user):
    try:
        return user.institute
    except (AttributeError, ObjectDoesNotExist):
        return None


def get_user_instructor(user):
    try:
        return user.instructor
    except (AttributeError, ObjectDoesNotExist):
        return None


            if not can_manage_exam(request.user, exam):
    if user == exam.created_by:
        return True
    instructor = get_user_instructor(user)
    if instructor and exam.course.instructor_id == instructor.id:
        return True
    institute = get_user_institute(user)
    if institute and exam.course.institute_id == institute.id:
        return True
    return False



@login_required
def exam_list(request):

    institute = get_user_institute(request.user)
    instructor = get_user_instructor(request.user)

    exams = Exam.objects.filter(is_active=True)
    if institute:
        exams = exams.filter(course__institute=institute)
    elif instructor:
        exams = exams.filter(course__instructor=instructor)
    else:
        exams = exams.filter(registrations__student=request.user)
    exams = exams.order_by('-created_at')

    return render(
        request,
        'course_exam/exam_list.html',
        {'exams': exams}
    )



@login_required
def create_exam(request):

    if request.method == 'POST':

        form = ExamForm(request.POST, user=request.user)

        if form.is_valid():

            exam = form.save(
                commit=False
            )

            exam.created_by = request.user

            exam.save()

            messages.success(
                request,
                'Exam created successfully.'
            )

            return redirect(
                'exam_list'
            )

    else:
        if get_user_institute(request.user) is None and get_user_instructor(request.user) is None:
            messages.error(request, 'You do not have permission to create exams.')
            return redirect('exam_list')

        form = ExamForm(user=request.user)

    return render(
        request,
        'course_exam/exam_create.html',
        {'form': form}
    )


@login_required
def exam_detail(request, pk):

    exam = get_object_or_404(
        Exam,
        pk=pk,
        is_active=True
    )

    if not can_manage_exam(request.user, exam) and request.user != exam.created_by:
        if not ExamRegistration.objects.filter(exam=exam, student=request.user).exists():
            messages.error(request, 'You are not allowed to access this exam.')
            return redirect('exam_list')

    registered_exam_ids = ExamRegistration.objects.filter(
        student=request.user
    ).values_list(
        'exam_id',
        flat=True
    )

    return render(
        request,
        'course_exam/exam_detail.html',
        {
            'exam': exam,
            'registered_exam_ids': registered_exam_ids,
            'now': timezone.now(),
        }
    )


@login_required
def edit_exam(request, pk):

    exam = get_object_or_404(
        Exam,
        pk=pk,
        is_active=True
    )

    if request.user != exam.created_by:
        messages.error(
            request,
            'You are not allowed to edit this exam.'
        )
        return redirect('exam_list')

    if request.method == 'POST':

        form = ExamForm(
            request.POST,
            instance=exam
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Exam updated successfully.'
            )

            return redirect(
                'exam_detail',
                pk=exam.pk
            )

    else:

        form = ExamForm(
            instance=exam
        )

    return render(
        request,
        'course_exam/exam_edit.html',
        {
            'form': form,
            'exam': exam
        }
    )


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Exam


@login_required
def delete_exam(request, pk):

    exam = get_object_or_404(
        Exam,
        pk=pk
    )

    if request.method == 'POST':

        exam.delete()

        messages.success(
            request,
            'Exam deleted successfully.'
        )

        return redirect('exam_list')

    return render(
        request,
        'course_exam/exam_delete.html',
        {
            'exam': exam
        }
    )



@login_required
def register_exam(request, pk):

    exam = get_object_or_404(
        Exam,
        pk=pk
    )
    if not exam.is_active:
        messages.error(request, 'Exam not available.')
        return redirect('exam_list')

    if timezone.now() > exam.registration_deadline:

        messages.error(
            request,
            "Registration deadline has passed."
        )

        return redirect(
            'exam_detail',
            pk=pk
        )

    registration, created = ExamRegistration.objects.get_or_create(
        exam=exam,
        student=request.user
    )

    if created:
        messages.success(
            request,
            "Successfully registered for the exam."
        )
    else:
        messages.info(
            request,
            "You are already registered."
        )

    return redirect(
        'exam_detail',
        pk=pk
    )



@login_required
def add_question(request, exam_id):

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    if not can_manage_exam(request.user, exam):
        messages.error(
            request,
            "Permission denied."
        )
        return redirect('exam_detail', exam.id)

    if request.method == 'POST':

        form = ExamQuestionForm(
            request.POST
        )

        if form.is_valid():

            question = form.save(
                commit=False
            )

            question.exam = exam
            question.save()

            question.exam.total_marks = sum(q.marks for q in question.exam.questions.all())

            question.exam.save()

            messages.success(
                request,
                "Question added successfully."
            )

            return redirect(
                'exam_questions',
                exam.id
            )

    else:

        form = ExamQuestionForm()

    return render(
        request,
        'course_exam/add_question.html',
        {
            'form': form,
            'exam': exam
        }
    )



@login_required
def exam_questions(request, exam_id):

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    if not can_manage_exam(request.user, exam):
        messages.error(request, 'Permission denied.')
        return redirect('exam_detail', exam.id)

    questions = exam.questions.all()

    return render(
        request,
        'course_exam/exam_questions.html',
        {
            'exam': exam,
            'questions': questions
        }
    )



@login_required
def edit_question(request, pk):

    question = get_object_or_404(
        ExamQuestion,
        pk=pk
    )

    exam = question.exam

    if not can_manage_exam(request.user, exam):
        messages.error(
            request,
            "Permission denied."
        )
        return redirect(
            'exam_questions',
            exam.id
        )

    if request.method == 'POST':

        form = ExamQuestionForm(
            request.POST,
            instance=question
        )

        if form.is_valid():

            form.save()

            exam.total_marks = sum(
                q.marks
                for q in exam.questions.all()
            )
            exam.save()

            messages.success(
                request,
                "Question updated successfully."
            )

            return redirect(
                'exam_questions',
                exam.id
            )

    else:

        form = ExamQuestionForm(
            instance=question
        )

    return render(
        request,
        'course_exam/edit_question.html',
        {
            'form': form,
            'question': question,
            'exam': exam
        }
    )


@login_required
def delete_question(request, pk):

    question = get_object_or_404(
        ExamQuestion,
        pk=pk
    )

    exam = question.exam

    if not can_manage_exam(request.user, exam):
        messages.error(
            request,
            "Permission denied."
        )
        return redirect(
            'exam_questions',
            exam.id
        )

    if request.method == 'POST':

        question.delete()

        exam.total_marks = sum(
            q.marks
            for q in exam.questions.all()
        )
        exam.save()

        messages.success(
            request,
            "Question deleted successfully."
        )

        return redirect(
            'exam_questions',
            exam.id
        )

    return render(
        request,
        'course_exam/delete_question.html',
        {
            'question': question,
            'exam': exam
        }
    )





@login_required
def student_exam_list(request):

    exams = Exam.objects.filter(
        is_active=True,
        start_datetime__gte=timezone.now()
    ).order_by('start_datetime')

    registered_exam_ids = ExamRegistration.objects.filter(
        student=request.user
    ).values_list(
        'exam_id',
        flat=True
    )

    return render(
        request,
        'course_exam/student_exam_list.html',
        {
            'exams': exams,
            'registered_exam_ids': registered_exam_ids,
            'now': timezone.now()
        }
    )



@login_required
def my_registered_exams(request):

    registrations = ExamRegistration.objects.filter(
        student=request.user
    ).select_related('exam')

    exams = []

    for reg in registrations:

        exam = reg.exam

        exams.append({
            'registration': reg,
            'exam': exam,
            'can_start':
                timezone.now() >=
                exam.start_datetime - timedelta(minutes=5)
        })

    return render(
        request,
        'course_exam/my_registered_exams.html',
        {
            'exams': exams,
            'now': timezone.now()
        }
    )


@login_required
def start_exam(request, exam_id):

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    registration = get_object_or_404(
        ExamRegistration,
        exam=exam,
        student=request.user
    )

    # Check if exam can be started (5 minutes before start time)
    exam_start_window = exam.start_datetime - timedelta(minutes=5)
    if timezone.now() < exam_start_window:
        messages.error(
            request,
            f"This exam can only be started 5 minutes before the scheduled start time. Available at: {exam_start_window.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        return redirect(
            'my_registered_exams'
        )

    attempt, created = ExamAttempt.objects.get_or_create(
        exam=exam,
        student=request.user,
        defaults={
            'total_marks': exam.total_marks
        }
    )

    # Already submitted?
    if attempt.is_submitted:

        messages.warning(
            request,
            "You have already submitted this exam."
        )

        return redirect(
            'view_answers',
            attempt.id
        )

    # Exam time expired?
    exam_end_time = min(
        attempt.started_at +
        timedelta(
            minutes=exam.duration_minutes
        ),
        exam.end_datetime
    )

    if timezone.now() > exam_end_time:

        attempt.is_submitted = True
        attempt.submitted_at = exam_end_time
        attempt.save()

        messages.warning(
            request,
            "Your exam time has expired."
        )

        return redirect(
            'view_answers',
            attempt.id
        )

    questions = exam.questions.all()

    return render(
        request,
        'course_exam/take_exam.html',
        {
            'exam': exam,
            'questions': questions,
            'attempt': attempt
        }
    )



@login_required
def submit_exam(request, exam_id):

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    # Allow only POST submissions
    if request.method != "POST":

        messages.error(
            request,
            "Invalid request."
        )

        return redirect(
            'start_exam',
            exam_id
        )

    attempt = get_object_or_404(
        ExamAttempt,
        exam=exam,
        student=request.user
    )

    # Already submitted
    if attempt.is_submitted:

        messages.warning(
            request,
            "You have already submitted this exam."
        )

        return redirect(
            'view_answers',
            attempt.id
        )

    # Check exam time limit
    exam_end_time = min(
        attempt.started_at +
        timedelta(
            minutes=exam.duration_minutes
        ),
        exam.end_datetime
    )

    # Time expired
    if timezone.now() > exam_end_time:

        attempt.is_submitted = True
        attempt.submitted_at = exam_end_time
        attempt.total_marks = exam.total_marks

        attempt.save()

        messages.warning(
            request,
            "Exam time has expired."
        )

        return redirect(
            'view_answers',
            attempt.id
        )

    score = 0

    # Save answers and calculate score
    for question in exam.questions.all():

        answer = request.POST.get(
            f"question_{question.id}"
        )

        StudentAnswer.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={
                'selected_answer': answer
            }
        )

        if answer == question.correct_answer:

            score += question.marks

    # Save attempt result
    attempt.score = score
    attempt.total_marks = exam.total_marks
    attempt.is_submitted = True
    attempt.submitted_at = timezone.now()

    attempt.save()

    messages.success(
        request,
        "Exam submitted successfully."
    )

    return redirect(
        'view_answers',
        attempt.id
    )


@login_required
def exam_registrations(request, exam_id):

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    if request.user != exam.created_by:

        institute = get_user_institute(request.user)
        if institute is None or exam.course.institute != institute:
            messages.error(
                request,
                "Permission denied."
            )
            return redirect(
                'exam_detail',
                exam.id
            )

        messages.error(
            request,
            "Permission denied."
        )

        return redirect(
            'exam_detail',
            exam.id
        )

    registrations = ExamRegistration.objects.filter(
        exam=exam
    ).select_related(
        'student'
    )

    # Fetch submitted attempts for this exam and map by student id
    attempts = ExamAttempt.objects.filter(
        exam=exam,
        is_submitted=True
    ).select_related('student')

    attempts_map = {a.student_id: a for a in attempts}

    # Build rows with registration and optional attempt
    rows = []
    for reg in registrations:
        attempt = attempts_map.get(reg.student_id)
        rows.append({
            'registration': reg,
            'student': reg.student,
            'attempt': attempt,
            'total_marks': exam.total_marks
        })

    return render(
        request,
        'course_exam/exam_registrations.html',
        {
            'exam': exam,
            'registrations': rows
        }
    )



@login_required
def view_answers(request, exam_id):

    exam = get_object_or_404(
        Exam,
        id=exam_id
    )

    if request.user != exam.created_by:

        messages.error(
            request,
            "Permission denied."
        )

        return redirect(
            'exam_detail',
            exam.id
        )

    attempts = ExamAttempt.objects.filter(
        exam=exam,
        is_submitted=True
    ).select_related(
        'student'
    )

    return render(
        request,
        'course_exam/exam_results.html',
        {
            'exam': exam,
            'attempts': attempts
        }
    )


@login_required
def exam_history(request):

    attempts = ExamAttempt.objects.filter(
        student=request.user,
        is_submitted=True
    ).select_related(
        'exam'
    )

    return render(
        request,
        'course_exam/exam_history.html',
        {
            'attempts': attempts
        }
    )


@login_required
def exam_results(request, attempt_id):

    attempt = get_object_or_404(
        ExamAttempt,
        id=attempt_id
    )

    answers = StudentAnswer.objects.filter(
        attempt=attempt
    ).select_related(
        'question'
    )

    return render(
        request,
        'course_exam/view_answers.html',
        {
            'attempt': attempt,
            'answers': answers
        }
    )
