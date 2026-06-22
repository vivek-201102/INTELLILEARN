from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.models import Institute
from courses.models import Instructor, Course, Enrollment


def _img(name='t.gif'):
    # 1x1 transparent GIF — enough to satisfy ImageField in tests.
    data = (b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!'
            b'\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01'
            b'\x00\x00\x02\x02D\x01\x00;')
    return SimpleUploadedFile(name, data, content_type='image/gif')


class IsolationAndAuthTests(TestCase):
    def setUp(self):
        # Institute A
        self.user_a = User.objects.create_user('inst_a', password='Pass!2345xyz')
        self.inst_a = Institute.objects.create(
            user=self.user_a, institute_name='A', contact='1', email='a@x.com')
        self.instr_a = Instructor.objects.create(
            name='IA', qualification='q', experience='1', profile_image=_img(),
            bio='b', institute=self.inst_a)
        self.course_a = Course.objects.create(
            title='CA', description='d', price=0, duration='1h',
            instructor=self.instr_a, thumbnail=_img(),
            what_you_will_learn='x', curriculum='y', institute=self.inst_a)

        # Institute B
        self.user_b = User.objects.create_user('inst_b', password='Pass!2345xyz')
        self.inst_b = Institute.objects.create(
            user=self.user_b, institute_name='B', contact='2', email='b@x.com')
        self.course_b = Course.objects.create(
            title='CB', description='d', price=0, duration='1h',
            instructor=self.instr_a, thumbnail=_img(),
            what_you_will_learn='x', curriculum='y', institute=self.inst_b)

    def test_anonymous_cannot_delete_course(self):
        resp = self.client.post(reverse('course_delete', args=[self.course_a.pk]))
        self.assertEqual(resp.status_code, 302)  # redirected to login
        self.assertTrue(Course.objects.filter(pk=self.course_a.pk).exists())

    def test_institute_cannot_edit_another_institutes_course(self):
        self.client.login(username='inst_b', password='Pass!2345xyz')
        resp = self.client.post(
            reverse('course_edit', args=[self.course_a.pk]),
            {'title': 'HACKED'})
        self.assertEqual(resp.status_code, 404)  # scoped queryset hides it
        self.course_a.refresh_from_db()
        self.assertEqual(self.course_a.title, 'CA')

    def test_institute_dashboard_counts_only_own_data(self):
        # Give B an enrollment that must NOT count for A.
        student = User.objects.create_user('stu', password='Pass!2345xyz')
        Enrollment.objects.create(student=student, course=self.course_b)

        self.client.login(username='inst_a', password='Pass!2345xyz')
        resp = self.client.get(reverse('institute_dashboard'))
        self.assertEqual(resp.context['total_courses'], 1)        # only CA
        self.assertEqual(resp.context['total_enrollments'], 0)    # B's enroll excluded

    def test_duplicate_enrollment_blocked(self):
        student = User.objects.create_user('stu2', password='Pass!2345xyz')
        Enrollment.objects.create(student=student, course=self.course_a)
        self.client.login(username='stu2', password='Pass!2345xyz')
        self.client.post(reverse('courses_enroll', args=[self.course_a.pk]))
        self.assertEqual(
            Enrollment.objects.filter(student=student, course=self.course_a).count(), 1)
