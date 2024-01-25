from django.contrib import admin
from django.urls import path

from .views import index, groups, about, students, teachers, login, show_student

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('students/', students, name='students'),
    path('student/<slug:stud_slug>/', show_student, name='student'),
    path('teachers/', teachers, name='teachers'),
    path('login/', login, name='login'),
    path('groups/<slug:group>/', groups),

]