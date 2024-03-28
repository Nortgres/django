from datetime import datetime
import pytz
from django.contrib.auth import get_user_model

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from students.models import Student, Group
from students.serializers import StudentSerializer, StudentDetailSerializer
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from students.views import teachers, StudentHome, ShowStudent

'''def calc(a, b, c):
    if c == '+':
        return a + b
    if c == '-':
        return a - b
    if c == '*':
        return a * b


class LogicTestCase(TestCase):
    def test_plus(self):
        result = calc(5, 7, '+')
        self.assertEqual(12, result)

    def test_minus(self):
        result = calc(5, 7, '-')
        self.assertEqual(-2, result)'''


class StudentsApiTestCase(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_superuser(username='admin', password='12345')
        self.user2 = User.objects.create(username='user')
        self.group1 = Group.objects.create(name='43', course='1', enrollment_year='2023')
        self.student1 = Student.objects.create(first_name='Иван', last_name='Зернов', middle_name='Иванович',
                        email='ivan@mail.ru', group_id=self.group1.id, slug='zernov', user=self.user1)
        self.student2 = Student.objects.create(first_name='Аркадий', last_name='Белов', middle_name='Акакиевич',
                        email='belov@mail.ru', group_id=self.group1.id, slug='belov', user=self.user1)
        self.students_url = reverse('students-list')
        self.student_url = reverse('students-detail', kwargs={'pk': self.student1.pk})

    def test_get(self):
        response = self.client.get(self.students_url)
        # print(f'{response.data=}')
        serializer_data = StudentSerializer([self.student2, self.student1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data['results'])

    def test_get_detail(self):
        response = self.client.get(self.student_url)
        # print(f'{response.data=}')
        serializer_data = StudentDetailSerializer(self.student1).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_delete(self):
        response = self.client.delete(self.student_url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.client.force_login(self.user2)
        response = self.client.delete(self.student_url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.client.force_login(self.user1)
        response = self.client.delete(self.student_url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        response = self.client.delete(self.student_url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_post_student(self):
        self.client.force_login(self.user1)
        with open("students/static/students/images/logo_zoloto_old.png", 'rb') as pict:
            data = {
                    'first_name': 'Екатерина',
                    'last_name': 'Смирнова',
                    'middle_name': 'Николаевна',
                    'email': 'katya@mail.ru',
                    'group': self.group1.id,
                    'slug': 'smirnova',
                    'photo': pict,
                    'user': self.user1.id
            }
            response = self.client.post(self.students_url, data)
            # print(f'{response.data=}')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)


class StudentsSerializerTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_superuser(username='admin', password='12345')
        self.user2 = User.objects.create(username='user')
        self.group1 = Group.objects.create(name='43', course='1', enrollment_year='2023')
        self.student1 = Student.objects.create(first_name='Иван', last_name='Зернов', middle_name='Иванович',
                        email='ivan@mail.ru', group_id=self.group1.id, slug='zernov', user=self.user1)
        self.student2 = Student.objects.create(first_name='Аркадий', last_name='Белов', middle_name='Акакиевич',
                        email='belov@mail.ru', group_id=self.group1.id, slug='belov', user=self.user1)
        self.students_url = reverse('students-list')
        self.student_url = reverse('students-detail', kwargs={'pk': self.student1.pk})

    def test_student_serializer(self):
        serializer_data = StudentSerializer([self.student1, self.student2], many=True).data
        expected_data = [
            {
                'last_name': 'Зернов',
                'first_name': 'Иван',
                'middle_name': 'Иванович',
                'email': 'ivan@mail.ru',
                'group': self.student1.group_id,
                'slug': 'zernov',
                'photo': None,
            },
            {
                'last_name': 'Белов',
                'first_name': 'Аркадий',
                'middle_name': 'Акакиевич',
                'email': 'belov@mail.ru',
                'group': self.student2.group_id,
                'slug': 'belov',
                'photo': None,
            }
        ]
        self.assertEqual(expected_data, serializer_data)

    def test_student_detail_serializer(self):
        serializer_data = StudentDetailSerializer(self.student1).data
        created_at_utc = self.student1.created_at.replace(tzinfo=pytz.utc)
        created_at = (str(created_at_utc.astimezone(pytz.timezone('Europe/Moscow')))).replace(' ', 'T')
        # created_at = self.student1.created_at.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        updated_at_utc = self.student1.created_at.replace(tzinfo=pytz.utc)
        updated_at = (str(updated_at_utc.astimezone(pytz.timezone('Europe/Moscow')))).replace(' ', 'T')
        # updated_at = self.student1.updated_at.astimezone(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        # print(f'{updated_at}')
        expected_data = [
            {
                'id': 1,
                'group_name': '1-43',
                'first_name': 'Иван',
                'last_name': 'Зернов',
                'middle_name': 'Иванович',
                'email': 'ivan@mail.ru',
                'birth_date': '2000-01-01',
                'created_at': created_at,
                'updated_at': updated_at,
                'is_study': True,
                'photo': None,
                'slug': 'zernov',
                'group': 1,
                'user': 1
            }
        ]
        # print(f'{expected_data[0]}')
        # print(f'{serializer_data}')
        self.assertEqual(expected_data[0], serializer_data)


class TestUrls(SimpleTestCase):

    def test_list_url_teachers(self):
        url = reverse('teachers')
        self.assertEqual(resolve(url).func, teachers)

    def test_list_url_home(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.view_class, StudentHome)

    def test_list_students(self):
        url = reverse('student', args=['smirnov145'])
        # print(resolve(url), resolve(url).func.view_class)
        # print(url)
        self.assertEqual(resolve(url).func.view_class, ShowStudent)


class BasicTests(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret')

        self.group1 = Group.objects.create(
            name='43',
            course='1',
            enrollment_year='2023')

        self.student1 = Student.objects.create(
            first_name='Иван',
            last_name='Зернов',
            middle_name='Иванович',
            email='ivan@mail.ru',
            group_id=self.group1.id,
            slug='zernov',
            user=self.user1)

        self.updatestudent_url = reverse('update_student', args=['1'])
        self.addstudent_url = reverse('addstudent')

    def test_string_representation(self):
        group = Group(
            name='44',
            course='2',
            enrollment_year='2022'
        )
        self.assertEqual(str(group), f'{group.course}-{group.name}')

    def test_group_content(self):
        self.assertEqual(f'{self.group1.name}', '43')
        self.assertEqual(f'{self.group1.course}', '1')
        self.assertEqual(f'{self.group1.enrollment_year}', '2023')

    def test_students_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Иван')
        self.assertContains(response, 'ЗЕРНОВ')
        # print(response.rendered_content)
        self.assertTemplateUsed(response, 'students/index.html')

    def test_student_detail_view(self):
        response = self.client.get('/student/zernov/')
        no_response = self.client.get('/student/grubov/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Иван')
        self.assertTemplateUsed(response, 'students/student.html')

    def test_get_absolute_url(self):
        self.assertEqual(self.student1.get_absolute_url(), '/student/zernov/')

    def test_student_create_view(self):
        self.client.force_login(self.user1)
        self.assertEqual(Student.objects.all().count(), 1)
        with open('students/static/students/images/logo_zoloto_old.png', 'rb') as pict:
            data = {
                'first_name': 'Екатерина',
                'last_name': 'Смирнова',
                'middle_name': 'Николаевна',
                'email': 'katya@mail.ru',
                'birth_date': '2000-10-18',
                'is_study': True,
                'group': self.group1.id,
                'slug': 'smirnova',
                'photo': pict,
                'user': self.user1.id
            }
            response = self.client.post(self.addstudent_url, data)
            print(response)
        self.assertEqual(status.HTTP_302_FOUND, response.status_code)
        self.assertEqual(Student.objects.filter(last_name='Смирнова').count(), 1)
        self.assertEqual(Student.objects.get(slug='smirnova').last_name, 'Смирнова')
        self.assertEqual(Student.objects.all().count(), 2)
