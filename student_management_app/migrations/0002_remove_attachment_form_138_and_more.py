# Generated by Django 5.1 on 2024-10-30 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='form_138',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='id_picture',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='psa',
        ),
    ]