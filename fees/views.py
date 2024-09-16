from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import (
    UserForm, StudentForm, StudentUpdateForm, UserUpdateForm, 
    DeactivateStudent, PaymentForm, PaymentUpdateForm, 
    PaymentFilterForm, StudentSearchForm,
    ComplaintFilterForm, ComplaintFixedForm
)
from .models import Student, Payment, Complaint, Staff, Faculty, Course
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required

from django.contrib.postgres.search import SearchVector

from django.core.paginator import Paginator




def index(request):
    '''===Logic Here ===
    - If user is authenticated, check if staff
    - If staff redirect to admin dashboard else user profile
    - If not authenticated redirect to login page
    '''
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('student_profile', username=request.user.username)
    else:
        return redirect('account_login')
    # return render(request, 'fees/index.html', {"title": "nile-home"})


@login_required
def admin_dashboard(request):
    '''
        - ** KEY LOGIC ** 
        - Admin section page
        - Rturns total students
        - Total Money
    '''
    # check if user is a staff
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    
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
    
    p = Paginator(Student.objects.all().filter(user__is_active=True).order_by('-added_date'), 10)
    page = request.GET.get('page')
    students = p.get_page(page)

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
    if query != None and query != '':
        students = Student.objects.annotate(search=SearchVector('user__last_name', 'user__username'),).filter(search__icontains=query)
        total_students = students.count()
        messages.success(
                request, f"{total_students} results has been returned."
        )
        
    context = {
        'students': students,
        'total_students': total_students,
        'd_form': deactivate_form,
        'filter_form': StudentSearchForm,
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


@login_required
def payment(request):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")

    p = Paginator(
            Payment.objects.all().order_by('-date_entered'), 10)
    page = request.GET.get('page')
    payments = p.get_page(page)
    pending_payments = Payment.objects.filter(status="pending")
    
    # Get staff object reuesting payment add
    staff = get_object_or_404(Staff, user=request.user)
    paymentFilterForm =  PaymentFilterForm
  
    if request.method == 'POST':
        p_form = PaymentForm(request.POST)
        
        if p_form.is_valid():
            p_form = p_form.save(commit=False)
            course_fee = p_form.student.courses.fee
            p_form.staff = staff

            # Return the student from form
            # Chek their last payment for that year & semester
            student = p_form.student
            payment = Payment.objects.filter(
                student=student, academic_year=p_form.academic_year, 
                semester=p_form.semester
            ).last()

            if (payment):
                p_form.balance = payment.balance - p_form.amount
            else:
                p_form.balance = course_fee -  p_form.amount

            #Check balnce after evaluation and set is_paid to true
            if(p_form.balance in [0, 0.0, 0.00]):
                p_form.is_paid = True

            p_form.status = 'confirmed'
            p_form.save()
            
            messages.success(
                request, f"Payment fee has been added for {student}"
            )

            return redirect(
                "make_payment"
            ) 
    p_form = PaymentForm()

    # Manage the filter form here.
    get_payment_id = request.GET.get('payment_id')
    get_start_date = request.GET.get('start_date')
    get_end_date = request.GET.get('end_date')

    if get_payment_id and get_payment_id != '':
       payments = Payment.objects.annotate(search=SearchVector('id'),).filter(search__icontains=get_payment_id)
    if get_start_date and get_payment_id != '':
        payments = Payment.objects.annotate(search=SearchVector('id'),).filter(search__gte=get_payment_id)
    if get_end_date and get_payment_id != '':
        payments = Payment.objects.annotate(search=SearchVector('id'),).filter(search__lt=get_payment_id)

    
    total_payments =  p.count # Count from paginations
    total_by_you = Payment.objects.filter(staff=staff).count()

    context = {
        'p_form': p_form,
        'payments': payments,
        'pending_payments': pending_payments,
        'total_payments': total_payments,
        'total_by_you': total_by_you,
        'total_pending': '',
        'title': 'nile-payment page',
        'paymentFilterForm': paymentFilterForm
    }
    return render(request, 'fees/payment.html', context)


@login_required
def update_payment(request, pk):
    '''
        - ** KEY LOGIC **
        - Update payment records
    '''
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

    form = PaymentFilterForm
    if 'query' in request.GET:
        form = PaymentFilterForm(request.GET)
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


@login_required
def payment_detail(request, id):
    payment = Payment.objects.get(id=id)
    context = {
        'payment':payment,
        'title': 'payment details'
    }
    return render(request, 'fees/payment_details.html', context)


# Search payments by id and academic year
# Using icontains to search for substrings of a full text
@login_required
def search_payments(request):
    payments = []
    form = PaymentFilterForm
    if 'query' in request.GET:
        form = PaymentFilterForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            if query.startswith('1'):
                query = query[3:]
            payments = Payment.objects.annotate(search=SearchVector('id', 'academic_year'),).filter(search__icontains=query)
           
    context ={
        'form': form,
        'payments': payments,
    }
    return render(request, 'fees/search_payment.html/', context)


def complaint_list(request):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    complaints = Complaint.objects.all().order_by('-date_submitted')
    FilterForm =  ComplaintFilterForm
    
    complaintFixedForm = ComplaintFixedForm(request.POST)
    if request.method =='POST':
        ref_code = request.POST.get('ref_code')
        
        if complaintFixedForm.is_valid():
            # Using the ref_code to get the exact complaint
            complaint = get_object_or_404(Complaint, reference_id=ref_code)
            complaint.status = complaintFixedForm.cleaned_data['status']
            complaint.save()
            messages.success(
                request, f"Comnplaint status updated."
            )
            return redirect(
                "complaint_list"
            ) 
    else:
        complaintFixedForm = ComplaintFixedForm()

    # Logic to filter complaints by reference id
    ref_id = request.GET.get('reference_id')
    if ref_id and ref_id != '':
        complaints = Complaint.objects.annotate(search=SearchVector('reference_id'),).filter(search__icontains=ref_id)

    # Logic to filter complaints by status
    status = request.GET.get('status')
    if status and status != '':
        complaints = Complaint.objects.annotate(search=SearchVector('status'),).filter(search__icontains=status)


    context={
        'complaints': complaints,
        'FilterForm': FilterForm,
        "complaintFixedForm": complaintFixedForm
    }
    return render(request, 'fees/complaint_list.html', context)

def complaint_details(request, slug):
    if not request.user.is_staff:
        messages.error(
                request, f"You do not have permission to access this page."
            )
        return redirect("/")
    complaint = complaint.objects.get(slug=slug)
    context={
        'complaint': complaint,
        'title': 'student-complaints'
    }
    return render(request, 'fees/complaint_details.html', context)


# return all faculties offered in school.
# with their courses.
def faculty(request):
    faculties = Faculty.objects.all()
    context = {
        'faculties': faculties
    }
    return render(request, 'fees/faculty.html', context)