from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import (
    UserForm, StudentForm, StudentUpdateForm, UserUpdateForm, 
    DeactivateStudent, PaymentForm, PaymentUpdateForm, 
    PaymentSearchForm, StudentSearchForm
)
from .models import Student, Payment, Remark, Staff, Faculty, Course
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

from django.contrib.postgres.search import SearchVector



def index(request):
    return render(request, 'fees/index.html', {"title": "nile-home"})

@login_required
def admin_dashboard(request):
    total_students = Student.objects.all().count()
    total_money = Payment.objects.aggregate(total=Sum('amount'))['total'] or 0
    context = {
        'total_students': total_students,
        'total_money': total_money,
        "title": "dashboard"
    }
    return render(request, 'fees/admin_dashboard.html', context)


@login_required
def student(request):

    '''
        - ** KEY LOGICS ** 
        - only for staffs && admins
        -  return all students
        - return total students
        - deactivate user by setting active to false
    '''

    # check if user is a staff
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    
    students = Student.objects.all().filter(user__is_active=True).order_by('-added_date')
    total_students =  Student.objects.all().filter(user__is_active=True).count() # total students

    # Search by filter
    filter_form = StudentSearchForm


    
    # get the username from the form using post
    # deactivate user
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

    # Logic to filter search list of students
    query = request.GET.get('query')
    if query and query != '':
        students = Student.objects.annotate(search=SearchVector('user__last_name', 'user__username'),).filter(search__icontains=query)
        print(students)

    context = {
        'students': students,
        'total_students': total_students,
        'd_form': deactivate_form,
        'filter_form': StudentSearchForm
    }
    return render(request, 'fees/all_students.html', context)


@login_required
def update_student(request, username):
    '''
        - ** KEY LOGICS ** 
        - only for staffs && admins
        - Update user dynamically
        - Returns form from 2 data models
        - Validate and update 2 data models
        - Redirect non admin with a message
    '''
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
            request.POST, request.FILES, instance=user.student_user
        )
        if u_form.is_valid() and stud_form.is_valid(): # check both form instances are valid 
            u_form.save()
            stud_form.save(commit=True)
            messages.success(request, f"{user.student_user} has been updated successfully.")
            return redirect(
                "students"
            ) 
        else:
            print("failed to update") 
    else:
        # Using the instances to return data back to the form field
        u_form = UserUpdateForm(instance=user)
        stud_form = StudentUpdateForm(instance=user.student_user)

    context = {"u_form": u_form, "stud_form": stud_form, 'title': 'update student'}
    return render(request, "fees/update_student.html", context)


@login_required
def addStudent(request):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    if request.method == 'POST':
        userform = UserForm(request.POST)
        studentform = StudentForm(request.POST, request.FILES)
        if userform.is_valid() and studentform.is_valid():
            userform.save(commit=False)
            user = userform.save()
            sform = studentform.save(commit=False)
            sform.user = user
            sform.save()
            messages.success(request, f"{user.student_user} has been added to record.")
            return redirect(
                "students"
            ) 
                      
    else:
        userform = UserForm()
        studentform = StudentForm()
    context = {
        'userform': userform,
        'studentform': studentform,
        'title': 'add student page'
    }
    return render(request, 'fees/addstudent.html', context)


def payment(request):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    
    if request.method == 'POST':
        p_form = PaymentForm(request.POST)
        # user = get_object_or_404(User, username=request.user.username)
        staff = get_object_or_404(Staff, user=request.user)
        

        if p_form.is_valid():
            p_form = p_form.save(commit=False)
            student = p_form.student
            payment = Payment.objects.filter(
                student=p_form.student, academic_year=p_form.academic_year, 
                semester=p_form.semester
            ).last()
            
            print(f"payment: {payment}")

            id = student.id
            course_fee = student.courses.fee

            p_form.staff = staff
            if (payment):
                p_form.balance = payment.balance - p_form.amount
            else:
                p_form.balance = course_fee -  p_form.amount

            p_form.save()
            
            messages.success(
                request, f"Payment fee has been added for student with id: {id}"
            )
            return redirect(
                "make_payment"
            ) 
    p_form = PaymentForm()

    payments = Payment.objects.all().order_by('-date_entered')
    total_payments =  Payment.objects.all().count()
    context = {
        'p_form': p_form,
        'payments': payments,
        'total_payments': total_payments,
        'title': 'nile-payment page'
    }
    return render(request, 'fees/payment.html', context)

@login_required
def update_payment(request, pk):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    payment = get_object_or_404(
            Payment, id=pk
        )
    if request.method == "POST":
        p_form = PaymentUpdateForm(
            request.POST, instance=payment
        )
        if p_form.is_valid():
            p_form.save()
            messages.success(
                request, f"Payment fee with id: {pk} has been updated."
            )
            return redirect(
                "make_payment"
            ) 
    else:
        p_form = PaymentUpdateForm(instance=payment)

    context = {"p_form": p_form}
    return render(request, "fees/update_payment.html", context)


@login_required
def delete_payment(request):

    '''
        ** KEY LOGIC **
        - delete payment
    '''

    # redirect if not admin  
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    
    if request.POST:
        id = request.POST.get('pay_id')
        # user = User.objects.get(username=username)
        Payment.objects.filter(pk=id).delete()
        
        messages.success(
            request, f"{id} has been deactivated."
        )
        return redirect(
                "make_payment"
        ) 


@login_required
def payment_report(request):

    '''
        ** KEY FEATURES **
        - return all reports and students
        - search functionalities
        - print payment report
    '''

    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")

    form = PaymentSearchForm
    if 'query' in request.GET:
        form = PaymentSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            if query.startswith('1'):
                query = query[3:]
            # payments = Payment.objects.annotate(search=SearchVector('id', 'academic_year'),).filter(search=query)
            # return redirect(reverse_lazy('search_payments'), payments)
            return redirect(f'/search/payment/?query={query}')
    else:
        payments = Payment.objects.all().order_by('-date_entered')
    
    context ={
        'payments': payments,
        'title': 'payments',
        'form': form
    }
    return render(request, 'fees/payment_report.html/', context)


def payment_detail(request, id):
    payment = Payment.objects.get(id=id)
    context = {
        'payment':payment,
        'title': 'payment details'
    }
    return render(request, 'fees/payment_details.html', context)

@login_required
def search_payments(request):
    payments = []
    form = PaymentSearchForm
    if 'query' in request.GET:
        form = PaymentSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            if query.startswith('1'):
                query = query[3:]
            payments = Payment.objects.annotate(search=SearchVector('id', 'academic_year'),).filter(search=query)
           
    context ={
        'form': form,
        'payments': payments,
    }
    return render(request, 'fees/search_payment.html/', context)


def remark_list(request):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    remarks = Remark.objects.all().order_by('-date')
    context={
        'remarks': remarks
    }
    return render(request, 'fees/remark_list.html', context)

def remark_details(request, slug):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    remark = Remark.objects.get(slug=slug)
    context={
        'remark': remark,
        'title': 'student-remarks'
    }
    return render(request, 'fees/remark_details.html', context)


def faculty(request):
    faculties = Faculty.objects.all()
    context = {
        'faculties': faculties
    }
    return render(request, 'fees/faculty.html', context)