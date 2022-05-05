from django.shortcuts import render
from .forms import UserForm, StudentForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'fees/index.html')


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
