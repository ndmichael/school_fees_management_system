from django.contrib import admin
from .models import (Faculty, Course, Student, Staff)
# Register your models here.

admin.site.register(Faculty)

admin.site.register(Course)

admin.site.register(Student)

admin.site.register(Staff)
