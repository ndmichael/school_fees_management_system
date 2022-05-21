from django.db import models
from django.contrib.auth.admin import User
from django.utils import timezone
import datetime
from smart_selects.db_fields import ChainedForeignKey # import from smart_select package


# Create your models here.

choices = (
        ('male', 'MALE'),
        ('female', 'FEMALE')
    )

class Faculty(models.Model):
    name = models.CharField(max_length= 150)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name


class Course(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length = 150)
    slug = models.SlugField(max_length=200)

    def __str__(self):
        return self.name


class Student (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='student_staff')
    faculty = models.ForeignKey(Faculty, on_delete = models.CASCADE, related_name='faculty')
    courses = ChainedForeignKey(
        Course,
        chained_field="faculty",
        chained_model_field = "faculty",
        show_all = False,
        auto_choose = True,
        sort = True
    )
    image = models.ImageField(default='avatar.png', upload_to='profile_pics/', blank=True, null=True)
    address  = models.TextField(max_length=1000)
    gender = models.CharField(choices = choices, max_length = 10, default="male")
    is_payed =  models.BooleanField(default=False)
    mobile_number = models.CharField(blank= True, max_length=15)
    admission_date = models.DateField(default=timezone.now)
    added_date  = models.DateTimeField(default=timezone.now)

    @property
    def fullname(self):
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/media/avatar.png"

    def __str__(self):
        return f'{self.user.username}'

 
class Staff(models.Model):
    DEPARTMENT = (
        ("admin", "ADMIN"),
    )
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='staff_user')
    image = models.ImageField(default='avatar.png', upload_to='profile_pics/', blank=False, null=False)
    address = models.TextField()
    mobileNo = models.CharField(blank= True, max_length = 15)
    DOB = models.DateField()
    gender = models.CharField(choices = choices, max_length = 20)
    department = models.CharField(choices =DEPARTMENT, default="admin", max_length=20)

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/media/avatar.png"
            
    def __str__(self):
            return f'{self.user.username}'


# def year_choices():
#     return [(r,r) for r in range(1990, datetime.date.today().year + 1)]

# print(year_choices)

def current_year():
    return datetime.date.today().year

class Payment(models.Model):
    
    sems = (
        ('semester 1', 'SEMESTER 1'),
        ('semester 2', 'SEMESTER 2')
    )
    p_method = (
        ('bank teller', 'BANK TELLER'),
        ('cash', 'CASH'),
        ('transfer', 'TRANSFER'),
        ('pos', 'POS')
    )
    year_choices = [(r,r) for r in range(2005, datetime.date.today().year + 1)]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="staff")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="staff")
    academic_year = models.PositiveIntegerField(choices = year_choices, default=current_year)
    semester = models.CharField(choices= sems, max_length=15, default='semester 1')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_entered = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(choices=p_method, max_length=15)

    def __str__(self):
        return f"{self.student}"
