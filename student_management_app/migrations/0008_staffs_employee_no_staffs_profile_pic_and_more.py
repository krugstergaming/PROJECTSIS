# Generated by Django 5.1 on 2024-09-05 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0007_sessionyearmodel_session_limit_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffs',
            name='employee_no',
            field=models.TextField(default=123456, max_length=6),
        ),
        migrations.AddField(
            model_name='staffs',
            name='profile_pic',
            field=models.FileField(default=1, upload_to='media'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffs',
            name='registration_date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='staffs',
            name='registration_no',
            field=models.TextField(default=123456, max_length=6),
        ),
        migrations.AddField(
            model_name='staffs',
            name='signature',
            field=models.FileField(default=1, upload_to='media'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staffs',
            name='teacher_license',
            field=models.FileField(default=1, upload_to='media'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='gradingconfiguration',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='parentguardian',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='previousschool',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='students',
            name='profile_pic',
            field=models.FileField(default=1, upload_to='media'),
            preserve_default=False,
        ),
    ]
