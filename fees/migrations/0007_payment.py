# Generated by Django 3.1.6 on 2022-05-20 21:13

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0006_auto_20220520_1543'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.PositiveIntegerField(choices=[(1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022)], default='')),
                ('semester', models.CharField(choices=[('semester 1', 'SEMESTER 1'), ('semester 2', 'SEMESTER 2')], max_length=15)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_entered', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_method', models.CharField(choices=[('bank teller', 'BANK TELLER'), ('cash', 'CASH'), ('transfer', 'TRANSFER'), ('pos', 'POS')], max_length=15)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='fees.staff')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='fees.student')),
            ],
        ),
    ]