from datetime import date
from django.db import models
from django.urls import reverse


class Student(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50)
    middle_name = models.CharField(verbose_name='Отчество', max_length=50)
    email = models.EmailField(verbose_name='e-mail', blank=True)
    birth_date = models.DateField(verbose_name='Дата рождения', default=date(2000, 1, 1))
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    is_study = models.BooleanField(verbose_name='Учится', default=True)
    photo = models.ImageField(verbose_name='Фото', upload_to="photos/%Y/%m/%d")
    group = models.ForeignKey('Group', on_delete=models.CASCADE, verbose_name='Группа', related_name='get_students')
    slug = models.SlugField(verbose_name='URL', max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.last_name

    def get_absolute_url(self):
        #return reverse('student', kwargs={'stud_id': self.pk})
        return reverse('student', kwargs={'stud_slug': self.slug})

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']

class Group(models.Model):
    name = models.CharField(verbose_name='Группа', max_length=5)
    course = models.CharField(verbose_name='Курс', max_length=2)
    enrollment_year = models.IntegerField(verbose_name='Год зачисления')

    def __str__(self):
        return f'{self.course}-{self.name}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'