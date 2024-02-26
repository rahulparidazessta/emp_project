# Generated by Django 5.0.1 on 2024-02-23 07:40

import django.db.models.deletion
import empmapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=15)),
                ('supervisor_name', models.CharField(max_length=100)),
                ('Description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('Name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('phone_num', models.CharField(max_length=10)),
                ('position', models.CharField(max_length=100)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, storage=empmapp.models.S3MediaStorage(), upload_to='')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='empmapp.department')),
            ],
        ),
        migrations.CreateModel(
            name='AttendenceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('check_in_time', models.TimeField()),
                ('check_out_timee', models.TimeField()),
                ('Present', models.BooleanField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='empmapp.employee')),
            ],
        ),
    ]
