# Generated by Django 5.1 on 2024-11-19 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0002_alter_staffs_citizenship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_employment_info',
            name='position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
