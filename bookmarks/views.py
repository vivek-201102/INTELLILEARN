from django.shortcuts import *
from django.contrib.auth.decorators import login_required

from .models import Bookmark
from courses.models import Course


@login_required
def toggle_bookmark(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    bookmark = Bookmark.objects.filter(
        student=request.user,
        course=course
    )

    if bookmark.exists():

        bookmark.delete()

    else:

        Bookmark.objects.create(
            student=request.user,
            course=course
        )

    return redirect(
        'course_detail',
        pk=course.id
    )


@login_required
def bookmarked_courses(request):

    bookmarks = Bookmark.objects.filter(
        student=request.user
    ).select_related(
        'course',
        'course__instructor'
    )

    return render(
        request,
        'bookmarks/bookmarked_courses.html',
        {
            'bookmarks': bookmarks
        }
    )