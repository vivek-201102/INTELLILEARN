from django.urls import path
from . import views

urlpatterns = [
     path('registration/', views.registration, name='registration'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
   
   
    path('institute_login_view/', views.institute_login_view, name='institute_login_view'),
    path('institute_register/', views.institute_register, name='institute_register'),
    
    path('institute-dashboard/', views.institute_dashboard, name='institute_dashboard'), 
    path('institute-logout/', views.institute_logout_view, name='institute_logout_view'),
 

]