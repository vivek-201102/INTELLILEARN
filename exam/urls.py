from django.urls import path
from . import views

urlpatterns = [

    # Add Quiz
    path(
        'courses/<int:course_pk>/add-quiz/',
        views.add_quiz,
        name='add_quiz'
    ),

    # Add Question
    path(
        'quiz/<int:quiz_pk>/add-question/',
        views.add_question,
        name='add_question'
    ),

    # View Quiz
path(
    'quiz/<int:quiz_pk>/',
    views.view_quiz,
    name='view_quiz'
),

# Edit Quiz
path(
    'quiz/edit/<int:pk>/',
    views.edit_quiz,
    name='edit_quiz'
),

# Delete Quiz
path(
    'quiz/delete/<int:pk>/',
    views.delete_quiz,
    name='delete_quiz'
),

# Edit Question
path(
    'question/edit/<int:pk>/',
    views.edit_question,
    name='edit_question'
),

# Delete Question
path(
    'question/delete/<int:pk>/',
    views.delete_question,
    name='delete_question'
),

path('quiz/<int:quiz_pk>/take/', views.take_quiz, name='take_quiz'),
    
   
path('quiz/review/<int:attempt_id>/', views.quiz_review_view, name='quiz_review'),

]