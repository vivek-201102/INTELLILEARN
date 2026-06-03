from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('courses/', views.course, name='courses'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('contact/', views.contact, name='contact'),
    path('my_courses/', views.my_courses,name='my_courses'),
       
    path(
    'instructor/dashboard/',
    views.instructor_dashboard,
    name='instructor_dashboard'),

    path(
        'instructor/courses/',
        views.instructor_courses,
        name='instructor_courses'
    ),

  path(
        'contact-messages/',
        views.contact_messages_list,
        name='contact_messages_list'
    ),
]