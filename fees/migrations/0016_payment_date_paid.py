# Generated by Django 3.1.6 on 2023-05-18 21:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0015_student_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='date_paid',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
