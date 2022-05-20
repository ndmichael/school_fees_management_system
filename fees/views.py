from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserForm, StudentForm, StudentUpdateForm, UserUpdateForm
from .models import Student
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'fees/index.html')


def student(request):
    students = Student.objects.all().filter(user__is_active=True).order_by('-added_date')
    total_students =  Student.objects.all().filter(user__is_active=True).count()
    context = {
        'students': students,
        'total_students': total_students
    }
    return render(request, 'fees/student.html', context)

@login_required
def update_student(request, username):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    user = get_object_or_404(
            User, username=username
        )
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        stud_form = StudentUpdateForm(
            request.POST, request.FILES, instance=user.student
        )
        if u_form.is_valid() and stud_form.is_valid():
            u_form.save()
            stud_form.save(commit=True)
            print("update success")
            return redirect(
                "students"
            ) 
        else:
            print("failed to update") 
    else:
        u_form = UserUpdateForm(instance=user)
        stud_form = StudentUpdateForm(instance=user.student)

    context = {"u_form": u_form, "stud_form": stud_form}
    return render(request, "fees/update_student.html", context)


@login_required
def addUser(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        studentform = StudentForm(request.POST, request.FILES)
        if userform.is_valid() and studentform.is_valid():
            userform.save(commit=False)
            user = userform.save()
            sform = studentform.save(commit=False)
            sform.user = user
            sform.save()
                      
    else:
        userform = UserForm()
        studentform = StudentForm()
    context = {
        'userform': userform,
        'studentform': studentform
    }
    return render(request, 'fees/adduser.html', context)
