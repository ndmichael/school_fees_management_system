# Generated by Django 4.2 on 2024-09-25 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0032_rename_complaint_payment_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='reference_id',
            field=models.CharField(default='eb6936a3-5037-48', editable=False, max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complaints', to='fees.student'),
        ),
    ]
