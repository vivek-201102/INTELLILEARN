from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from courses.models import Course
from courses.permissions import user_can_manage_course, course_manage_denied_response
from .models import Question, Quiz


def _deny_quiz_manage(request, quiz):
    return course_manage_denied_response(request, quiz.course)

# Create your views here.
@login_required
def add_quiz(request, course_pk):

    course = get_object_or_404(
        Course,
        pk=course_pk
    )

    denied = course_manage_denied_response(request, course)
    if denied:
        return denied

    if request.method == "POST":

        title = request.POST.get('title')

        quiz = Quiz.objects.create(
            course=course,
            title=title
        )

        messages.success(
            request,
            "Quiz created successfully."
        )

        return redirect(
            'add_question',
            quiz_pk=quiz.pk
        )

    return render(
        request,
        'exam/add_quiz.html',
        {
            'course': course
        }
    )



@login_required
def add_question(request, quiz_pk):

    quiz = get_object_or_404(
        Quiz.objects.select_related('course'),
        pk=quiz_pk
    )
    denied = _deny_quiz_manage(request, quiz)
    if denied:
        return denied

    questions = quiz.questions.all()

    if request.method == "POST":
        action = request.POST.get('action', 'add')

        if action == 'finish':
            if not questions.exists():
                messages.warning(
                    request,
                    "Add at least one question before finishing the quiz."
                )
                return redirect('add_question', quiz_pk=quiz.pk)

            messages.success(
                request,
                f'Quiz "{quiz.title}" is complete and published.'
            )
            return redirect('view_quiz', quiz_pk=quiz.pk)

        question_text = request.POST.get('question', '').strip()
        option1 = request.POST.get('option1', '').strip()
        option2 = request.POST.get('option2', '').strip()
        option3 = request.POST.get('option3', '').strip()
        option4 = request.POST.get('option4', '').strip()
        correct_answer = request.POST.get('correct_answer', '').strip()

        if not all([question_text, option1, option2, option3, option4, correct_answer]):
            messages.error(request, "Please fill in all fields.")
            return redirect('add_question', quiz_pk=quiz.pk)

        valid_answers = {option1, option2, option3, option4}
        if correct_answer not in valid_answers:
            messages.error(
                request,
                "Correct answer must match one of the four options exactly."
            )
            return redirect('add_question', quiz_pk=quiz.pk)

        Question.objects.create(
            quiz=quiz,
            question=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer=correct_answer,
        )

        messages.success(
            request,
            "Question added. Add another below, or finish the quiz."
        )
        return redirect('add_question', quiz_pk=quiz.pk)

    return render(
        request,
        'exam/add_question.html',
        {
            'quiz': quiz,
            'course': quiz.course,
            'questions': questions,
        }
    )


@login_required
def view_quiz(request, quiz_pk):

    quiz = get_object_or_404(
        Quiz.objects.select_related('course'),
        pk=quiz_pk
    )

    questions = quiz.questions.all()
    can_manage_course = user_can_manage_course(request.user, quiz.course)

    return render(
        request,
        'exam/view_quiz.html',
        {
            'quiz': quiz,
            'course': quiz.course,
            'questions': questions,
            'can_manage_course': can_manage_course,
        }
    )


@login_required
def edit_question(request, pk):

    question = get_object_or_404(
        Question.objects.select_related('quiz__course'),
        pk=pk
    )

    denied = _deny_quiz_manage(request, question.quiz)
    if denied:
        return denied

    if request.method == "POST":

        question.question = request.POST.get('question')

        question.option1 = request.POST.get('option1')

        question.option2 = request.POST.get('option2')

        question.option3 = request.POST.get('option3')

        question.option4 = request.POST.get('option4')

        question.correct_answer = request.POST.get(
            'correct_answer'
        )

        question.save()

        messages.success(
            request,
            "Question updated successfully."
        )

        return redirect(
            'view_quiz',
            quiz_pk=question.quiz.pk
        )

    return render(
        request,
        'exam/edit_question.html',
        {
            'question': question
        }
    )



@login_required
def delete_question(request, pk):

    question = get_object_or_404(
        Question.objects.select_related('quiz__course'),
        pk=pk
    )

    denied = _deny_quiz_manage(request, question.quiz)
    if denied:
        return denied

    quiz_pk = question.quiz.pk

    if request.method == "POST":

        question.delete()

        messages.success(
            request,
            "Question deleted successfully."
        )

        return redirect(
            'view_quiz',
            quiz_pk=quiz_pk
        )

    return render(
        request,
        'exam/delete_question.html',
        {
            'question': question
        }
    )



@login_required
def edit_quiz(request, pk):

    quiz = get_object_or_404(
        Quiz.objects.select_related('course'),
        pk=pk
    )

    denied = _deny_quiz_manage(request, quiz)
    if denied:
        return denied

    if request.method == "POST":

        quiz.title = request.POST.get('title')

        quiz.save()

        messages.success(
            request,
            "Quiz updated successfully."
        )

        return redirect(
            'view_quiz',
            quiz_pk=quiz.pk
        )

    return render(
        request,
        'exam/edit_quiz.html',
        {
            'quiz': quiz
        }
    )



@login_required
def delete_quiz(request, pk):

    quiz = get_object_or_404(
        Quiz.objects.select_related('course'),
        pk=pk
    )

    denied = _deny_quiz_manage(request, quiz)
    if denied:
        return denied

    course_pk = quiz.course.pk

    if request.method == "POST":

        quiz.delete()

        messages.success(
            request,
            "Quiz deleted successfully."
        )

        from django.urls import reverse
        return redirect(
            reverse('course_detail', kwargs={'pk': course_pk}) + '?tab=quiz'
        )

    return render(
        request,
        'exam/delete_quiz.html',
        {
            'quiz': quiz
        }
    )