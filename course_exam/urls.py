from django.urls import path
from . import views


urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('create/', views.create_exam, name='create_exam'),
    path('exam-detail/<int:pk>/', views.exam_detail, name='exam_detail'),
    path('<int:pk>/edit/', views.edit_exam, name='edit_exam'),
    path('<int:pk>/delete/', views.delete_exam, name='delete_exam'),

    path(
    '<int:exam_id>/questions/',
    views.exam_questions,
    name='exam_questions'
),

path(
    '<int:exam_id>/questions/add/',
    views.add_question,
    name='add_question'
),

path(
    'question/<int:pk>/edit/',
    views.edit_question,
    name='edit_question'
),

path(
    'question/<int:pk>/delete/',
    views.delete_question,
    name='delete_question'
),

# urls.py

path(
    'student/exams/',
    views.student_exam_list,
    name='student_exam_list'
),

path(
    '<int:pk>/register/',
    views.register_exam,
    name='register_exam'
),

path(
    'student/my-exams/',
    views.my_registered_exams,
    name='my_registered_exams'
),


path(
    '<int:exam_id>/start/',
    views.start_exam,
    name='start_exam'
),

path(
    '<int:exam_id>/submit/',
    views.submit_exam,
    name='submit_exam'
),


path(
    '<int:exam_id>/registrations/',
    views.exam_registrations,
    name='exam_registrations'
),

path(
    '<int:exam_id>/results/',
    views.exam_results,
    name='exam_results'
),


path(
    'student/history/',
    views.exam_history,
    name='exam_history'
),

path(
    'attempt/<int:attempt_id>/answers/',
    views.view_answers,
    name='view_answers'
),


]