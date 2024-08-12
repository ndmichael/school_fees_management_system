from django.contrib import admin
from .models import (Faculty, Course, Student, Staff, Payment, Complaint)
# Register your models here.

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "faculty", "fee")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("user", "faculty", "courses", "gender",  "admission_date")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "mobileNo", "gender", "gender", "department")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("academic_year", "semester", "amount", "date_entered","is_paid", "is_confirmed", "image", "payment_method", "student")


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("subject", "description", "date_submitted", "student")
