from django.contrib import admin
from .models import (Faculty, Course, StudentProfile, StaffProfile)
# Register your models here.

admin.site.register(Faculty)

admin.site.register(Course)

admin.site.register(StudentProfile)

admin.site.register(StaffProfile)
