from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Question, Quiz
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
@login_required
def add_quiz(request, course_pk):

    course = get_object_or_404(
        Course,
        pk=course_pk
    )

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
        Quiz,
        pk=quiz_pk
    )

    if request.method == "POST":

        Question.objects.create(

            quiz=quiz,

            question=request.POST.get('question'),

            option1=request.POST.get('option1'),

            option2=request.POST.get('option2'),

            option3=request.POST.get('option3'),

            option4=request.POST.get('option4'),

            correct_answer=request.POST.get('correct_answer')
        )

        messages.success(
            request,
            "Question added successfully."
        )

        return redirect(
            'add_question',
            quiz_pk=quiz.pk
        )

    return render(
        request,
        'exam/add_question.html',
        {
            'quiz': quiz
        }
    )


def view_quiz(request, quiz_pk):

    quiz = get_object_or_404(
        Quiz,
        pk=quiz_pk
    )

    questions = quiz.questions.all()

    return render(
        request,
        'exam/view_quiz.html',
        {
            'quiz': quiz,
            'questions': questions
        }
    )


@login_required
def edit_question(request, pk):

    question = get_object_or_404(
        Question,
        pk=pk
    )

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
        Question,
        pk=pk
    )

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
        Quiz,
        pk=pk
    )

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
        Quiz,
        pk=pk
    )

    course_pk = quiz.course.pk

    if request.method == "POST":

        quiz.delete()

        messages.success(
            request,
            "Quiz deleted successfully."
        )

        return redirect(
            'course_detail',
            pk=course_pk
        )

    return render(
        request,
        'exam/delete_quiz.html',
        {
            'quiz': quiz
        }
    )