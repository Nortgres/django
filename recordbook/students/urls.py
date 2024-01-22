from django.contrib import admin
from django.urls import path

from .views import index, groups, about, students, teachers, login

urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),
    path('students/', students, name='students'),
    path('teachers/', teachers, name='teachers'),
    path('login/', login, name='login'),
    path('groups/<slug:group>/', groups),

]