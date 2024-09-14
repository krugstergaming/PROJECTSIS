# Generated by Django 5.1 on 2024-09-10 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffs',
            name='age',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='staffs',
            name='tin_id',
            field=models.CharField(blank=True, default='N/A', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='students',
            name='Enrollment_status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='gsis_id',
            field=models.CharField(blank=True, default='N/A', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='pagibig_id',
            field=models.CharField(blank=True, default='N/A', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='philhealth_id',
            field=models.CharField(blank=True, default='N/A', max_length=50, null=True),
        ),
    ]
