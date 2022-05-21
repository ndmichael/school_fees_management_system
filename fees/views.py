from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import (
    UserForm, StudentForm, StudentUpdateForm, UserUpdateForm, 
    DeactivateStudent, PaymentForm
)
from .models import Student
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'fees/index.html')


def student(request):
    if request.POST:
        username = request.POST.get('username')
        # user = User.objects.get(username=username)
        user = get_object_or_404(User, username=username)
        if  request.POST.get('deactivate') == 'on':
            user.is_active = False
            user.save()
            messages.success(
                request, f"{username} has been deactivated."
            )
        return redirect(
                "students"
            )  
    else:
        deactivate_form = DeactivateStudent()
    students = Student.objects.all().filter(user__is_active=True).order_by('-added_date')
    total_students =  Student.objects.all().filter(user__is_active=True).count()
    context = {
        'students': students,
        'total_students': total_students,
        'd_form': deactivate_form
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


def payment(request):
    # print(request.user.staff_user)
    if request.method == 'POST':
        p_form = PaymentForm(request.POST)
        if p_form.is_valid():
            p_form = p_form.save(commit=False)
            p_form.staff = request.user.staff_user
            p_form.save()
            id = p_form.student
            messages.success(
                request, f"Payment fee has been added for student with id: {id}"
            )
            return redirect(
                "make_payment"
            ) 
    p_form = PaymentForm()
    context = {'p_form': p_form}
    return render(request, 'fees/payment.html', context)