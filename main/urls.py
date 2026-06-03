from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'instructor-dashboard/',
        views.InstructorDashboardRedirect.as_view(),
        name='instructor_dashboard',
    ),
]
