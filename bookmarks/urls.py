from django.urls import path
from . import views

urlpatterns = [

    path(
        'toggle/<int:course_id>/',
        views.toggle_bookmark,
        name='toggle_bookmark'
    ),

    path(
        'my-bookmarks/',
        views.bookmarked_courses,
        name='bookmarked_courses'
    ),

]