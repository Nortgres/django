from django.contrib import admin
from django.urls import path
from .views import index, groups, about

urlpatterns = [
    path('', index),
    path('groups/<slug:group>/', groups),
    path('about/', about),
]