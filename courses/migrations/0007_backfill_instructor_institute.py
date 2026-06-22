from django.db import migrations


def backfill_instructor_institute(apps, schema_editor):
    """
    Existing instructors predate the Instructor.institute field. Assign each
    one the institute of a course they teach, so they remain visible to and
    manageable by that institute after data isolation was introduced.
    """
    Instructor = apps.get_model('courses', 'Instructor')
    Course = apps.get_model('courses', 'Course')

    for instructor in Instructor.objects.filter(institute__isnull=True):
        course = (
            Course.objects
            .filter(instructor=instructor, institute__isnull=False)
            .first()
        )
        if course is not None:
            instructor.institute_id = course.institute_id
            instructor.save(update_fields=['institute'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_instructor_institute_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_instructor_institute, noop),
    ]
