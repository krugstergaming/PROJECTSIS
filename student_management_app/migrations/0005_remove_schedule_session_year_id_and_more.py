# Generated by Django 5.1 on 2024-11-25 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0004_customuser_last_login_session_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='session_year_id',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='staff_id',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='blood_type',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='cellphone_no',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='gsis_id',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='height',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='pagibig_id',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='permanent_address',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='philhealth_id',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='sss_id',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='telephone_no',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='tin_id',
        ),
        migrations.RemoveField(
            model_name='staffs',
            name='weight',
        ),
        migrations.AddField(
            model_name='enrollment',
            name='GradeLevel_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.gradelevel'),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='citizenship',
            field=models.CharField(blank=True, default='Filipino', max_length=20, null=True),
        ),
        migrations.CreateModel(
            name='Enrollment_voucher',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('registration_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('misc_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('tuition_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('GradeLevel_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.gradelevel')),
            ],
        ),
        migrations.CreateModel(
            name='staff_contact_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(blank=True, max_length=255, null=True)),
                ('province', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('barangay', models.CharField(blank=True, max_length=255, null=True)),
                ('street', models.CharField(blank=True, max_length=255, null=True)),
                ('telephone_no', models.CharField(blank=True, max_length=20, null=True)),
                ('cellphone_no', models.CharField(blank=True, max_length=20, null=True)),
                ('emergency_contact', models.CharField(blank=True, max_length=20, null=True)),
                ('emergency_relationship', models.CharField(blank=True, max_length=255, null=True)),
                ('medical_condition', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staffs_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='staff_employment_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_number', models.CharField(blank=True, editable=False, max_length=12, null=True, unique=True)),
                ('employee_type', models.CharField(blank=True, max_length=255, null=True)),
                ('position', models.CharField(blank=True, max_length=255, null=True)),
                ('employment_status', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staffs_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='staff_government_ID_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gsis_id', models.CharField(blank=True, default='N/A', max_length=50, null=True)),
                ('pagibig_id', models.CharField(blank=True, default='N/A', max_length=50, null=True)),
                ('philhealth_id', models.CharField(blank=True, default='N/A', max_length=50, null=True)),
                ('sss_id', models.CharField(blank=True, default='N/A', max_length=50, null=True)),
                ('tin_id', models.CharField(blank=True, default='N/A', max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staffs_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='staff_physical_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_type', models.CharField(blank=True, max_length=10, null=True)),
                ('height', models.CharField(blank=True, max_length=10, null=True)),
                ('weight', models.CharField(blank=True, max_length=10, null=True)),
                ('eye_color', models.CharField(blank=True, max_length=255, null=True)),
                ('hair_color', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staffs_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='Staffs_Educ_Background',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HEA', models.CharField(blank=True, max_length=255, null=True)),
                ('Cert_License', models.CharField(blank=True, max_length=255, null=True)),
                ('teaching_exp', models.CharField(blank=True, max_length=255, null=True)),
                ('skills_competencies', models.CharField(blank=True, max_length=255, null=True)),
                ('language_spoken', models.CharField(blank=True, max_length=255, null=True)),
                ('preferred_subject', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staffs_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
            ],
        ),
    ]
