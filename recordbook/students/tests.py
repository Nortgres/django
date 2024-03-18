from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

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
    def test_get(self):
        url = reverse('students-list')
        print(f'{url=}')
        response = self.client.get(url)
        print(f'{response=}')
