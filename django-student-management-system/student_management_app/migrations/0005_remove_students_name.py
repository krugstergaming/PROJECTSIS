# Generated by Django 5.1 on 2024-09-02 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0004_students_age_students_date_of_birth_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='name',
        ),
    ]