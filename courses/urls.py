from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # Instructor URLs
    # =========================
    path(
        'instructor_list/',
        views.instructor_list,
        name='instructor_list'
    ),

    path(
        'add/',
        views.instructor_create,
        name='instructor_create'
    ),

    path(
        '<int:pk>/edit/',
        views.instructor_edit,
        name='instructor_edit'
    ),

    path(
        '<int:pk>/delete/',
        views.instructor_delete,
        name='instructor_delete'
    ),

    path(
        '<int:pk>/',
        views.instructor_detail,
        name='instructor_detail'
    ),


    # =========================
    # Course URLs
    # =========================
    path(
        'courses/',
        views.course_list,
        name='course_list'
    ),

    path(
        'courses/add/',
        views.course_create,
        name='course_create'
    ),

    path(
        'courses/<int:pk>/edit/',
        views.course_edit,
        name='course_edit'
    ),

    path(
        'courses/<int:pk>/delete/',
        views.course_delete,
        name='course_delete'
    ),


    # =========================
    # Notes URLs
    # =========================

    # Add Note
    path(
        'courses/<int:pk>/add-note/',
        views.manage_note,
        name='add_note'
    ),

    # Edit Note
    path(
        'course/<int:course_pk>/note/edit/<int:note_pk>/',
        views.manage_note,
        name='edit_note'
    ),


    # =========================
    # Course Purchase
    # =========================
    path(
        'course/<int:pk>/enroll/',
        views.courses_enroll,
        name='courses_enroll'
    ),


    # =========================
    # Students
    # =========================
    path(
        'institute/student/',
        views.institute_students,
        name='institute_students'
    ),

    path(
        'course/<int:pk>/students/',
        views.course_students,
        name='course_students'
    ),


    # =========================
    # Course Detail
    # KEEP LAST
    # =========================
    path(
        'courses/<int:pk>/',
        views.course_detail,
        name='course_detail'
    ),
]