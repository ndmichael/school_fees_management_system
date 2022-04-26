from django.db import models
from django.contrib.auth.admin import User
from django.utils import timezone
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


class StudentProfile (models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete = models.CASCADE)
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
    gender = models.CharField(choices = choices, max_length = 10)
    mobile_number = models.CharField(blank= True, max_length=15)
    admission_date = models.DateField(default=timezone.now)
    record_date  = models.DateTimeField(default=timezone.now)

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "/media/avatar.png"

    def __str__(self):
        return f'{self.user.username}'

 
class StaffProfile(models.Model):
    DEPARTMENT = (
        ("admin", "ADMIN"),
    )
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(default='avatar.png', upload_to='profile_pics/', blank=True, null=True)
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


