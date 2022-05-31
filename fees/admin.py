from django.contrib import admin
from .models import (Faculty, Course, Student, Staff, Payment, Remark)
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
    list_display = ("user", "faculty", "courses", "gender", "is_payed", "admission_date")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user", "address", "mobileNo", "gender", "gender", "department")

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("academic_year", "semester", "amount", "date_entered", "payment_method", "student")


@admin.register(Remark)
class RemarkAdmin(admin.ModelAdmin):
    list_display = ("subject", "body", "date", "student")
