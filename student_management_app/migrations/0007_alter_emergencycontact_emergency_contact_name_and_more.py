# Generated by Django 5.1 on 2024-09-13 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0006_rename_address_emergencycontact_emergency_contact_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencycontact',
            name='emergency_contact_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='emergency_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
