# Generated by Django 5.1 on 2024-11-19 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffs',
            name='citizenship',
            field=models.CharField(blank=True, default='Filipino', max_length=20, null=True),
        ),
    ]
