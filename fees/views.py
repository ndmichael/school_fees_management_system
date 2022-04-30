from django.shortcuts import render
from .forms import UserForm, StudentForm

# Create your views here.

def index(request):
    return render(request, 'fees/index.html')


def addUser(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        studentform = StudentForm(request.POST)
        if userform.is_valid() and studentform.is_valid():
            userform.save()
            sform = studentform.save(False)
            sform.user = userform.id
            sform.save()
    else:
        userform = UserForm()
        studentform = StudentForm()
    context = {
        'userform': userform,
        'studentform': studentform
    }
    return render(request, 'fees/adduser.html', context)
