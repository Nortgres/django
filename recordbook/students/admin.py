from typing import Tuple

from django.contrib import admin
from .models import Student, Group

# Register your models here.

#admin.site.register(Student)
admin.site.register(Group)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'last_name', 'first_name', 'created_at', 'is_study', 'photo')
    list_display_links = ('id', 'last_name')
    search_fields = ('last_name', 'first_name')
    list_editable = ('is_study',)
    list_filter = ('is_study', 'created_at')
    prepopulated_fields = {"slug": ("last_name", )}

admin.site.register(Student, StudentAdmin)