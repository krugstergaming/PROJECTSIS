# Generated by Django 5.1 on 2024-11-27 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0002_alter_staff_contact_info_adminhod_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='school_info',
            name='barangay',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school_info',
            name='city',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school_info',
            name='province',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school_info',
            name='region',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school_info',
            name='school_cellphone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='school_info',
            name='school_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='school_info',
            name='school_telephone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='school_info',
            name='street',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
