# Generated by Django 5.1 on 2024-10-21 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0002_rename_assignsection_load_assignsection_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='load',
            name='GradeLevel_id',
        ),
    ]