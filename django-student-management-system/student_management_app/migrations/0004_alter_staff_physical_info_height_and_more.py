# Generated by Django 5.1 on 2024-11-19 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0003_alter_staff_employment_info_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_physical_info',
            name='height',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='staff_physical_info',
            name='weight',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
