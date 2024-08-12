import json
from django.core.management.base import BaseCommand
from fees.models import Student, Faculty, Course  # Adjust to your app's name
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Load student data from a JSON file'

    def handle(self, *args, **kwargs):
        with open('fees/fixtures/students.json') as f:
            students = json.load(f)

        for student_data in students:
            user_data = student_data['user']
            user = User.objects.create_user(
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                email=user_data['email'],
                password=user_data['password']
            )

            faculty = Faculty.objects.get(id=student_data['faculty_id'])
            course = Course.objects.get(id=student_data['course_id'])

            student = Student.objects.create(
                user=user,
                faculty=faculty,
                courses=course,
                address=student_data['address'],
                gender=student_data['gender'],
                mobile_number=student_data['mobile_number'],
                dob=student_data['dob'],
                admission_date=student_data['admission_date']
            )
            student.save()

        self.stdout.write(self.style.SUCCESS('Successfully loaded student data into the database'))
