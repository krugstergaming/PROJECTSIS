# Generated by Django 5.1 on 2024-11-25 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0005_remove_schedule_session_year_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='School_info',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('school_name', models.CharField(blank=True, max_length=255, null=True)),
                ('school_ID_number', models.CharField(blank=True, max_length=255, null=True)),
                ('school_district', models.CharField(blank=True, max_length=255, null=True)),
                ('school_division', models.CharField(blank=True, max_length=255, null=True)),
                ('school_region', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
