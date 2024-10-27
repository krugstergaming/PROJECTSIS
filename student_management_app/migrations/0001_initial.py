# Generated by Django 5.1 on 2024-10-25 14:54

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculums',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('curriculum_name', models.CharField(max_length=255)),
                ('curriculum_description', models.TextField(max_length=255)),
                ('curriculum_status', models.CharField(max_length=255)),
                ('is_archived', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('registration_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('misc_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('tuition_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('downpayment', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('discount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('discount_amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('installment_option', models.CharField(blank=True, default='Monthly', max_length=50, null=True)),
                ('installment_payment', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True)),
                ('assessed_by', models.CharField(blank=True, max_length=100, null=True)),
                ('assessed_date', models.DateField(blank=True, null=True)),
                ('payment_received_by', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('enrollment_status', models.CharField(default='Pending', max_length=20)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GradingConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_grading_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SessionYearModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('session_start_year', models.DateField(blank=True, null=True)),
                ('session_end_year', models.DateField(blank=True, null=True)),
                ('session_limit', models.IntegerField(blank=True, null=True)),
                ('session_status', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[(1, 'HOD'), (2, 'Staff'), (3, 'Student')], default=1, max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdminHOD',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BalancePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_balance_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_balance_date', models.DateField(blank=True, null=True)),
                ('past_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remarks', models.TextField(blank=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='student_management_app.enrollment')),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_picture', models.CharField(blank=True, max_length=255, null=True)),
                ('id_picture_file', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('psa', models.CharField(blank=True, max_length=255, null=True)),
                ('psa_file', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('form_138', models.CharField(blank=True, max_length=255, null=True)),
                ('form_138_file', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('attachment_remarks', models.CharField(blank=True, max_length=255, null=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='student_management_app.enrollment')),
            ],
        ),
        migrations.CreateModel(
            name='GradeLevel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('GradeLevel_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('curriculum_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.curriculums')),
            ],
        ),
        migrations.CreateModel(
            name='AssignSection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('GradeLevel_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.gradelevel')),
            ],
        ),
        migrations.CreateModel(
            name='Load',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('is_advisory', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('AssignSection_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.assignsection')),
                ('curriculum_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.curriculums')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('section_name', models.CharField(max_length=255)),
                ('section_limit', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('GradeLevel_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.gradelevel')),
            ],
        ),
        migrations.AddField(
            model_name='assignsection',
            name='section_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.section'),
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('day_of_week', models.CharField(max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('load_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.load')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('session_year_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.sessionyearmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('session_year_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.sessionyearmodel')),
            ],
        ),
        migrations.CreateModel(
            name='Staffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('suffix', models.CharField(blank=True, max_length=20, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('age', models.CharField(blank=True, max_length=15, null=True)),
                ('pob', models.CharField(max_length=255)),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('civil_status', models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('other', 'Other')], max_length=20)),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('blood_type', models.CharField(blank=True, max_length=10, null=True)),
                ('gsis_id', models.CharField(blank=True, default='N/A', max_length=50, null=True)),
                ('pagibig_id', models.CharField(blank=True, default='N/A', max_length=50, null=True)),
                ('philhealth_id', models.CharField(blank=True, default='N/A', max_length=50, null=True)),
                ('sss_id', models.CharField(blank=True, default='N/A', max_length=50, null=True)),
                ('tin_id', models.CharField(blank=True, default='N/A', max_length=50, null=True)),
                ('citizenship', models.CharField(choices=[('filipino', 'Filipino'), ('dual', 'Dual Citizenship')], max_length=20)),
                ('dual_country', models.CharField(blank=True, max_length=255, null=True)),
                ('permanent_address', models.TextField(blank=True, null=True)),
                ('telephone_no', models.CharField(blank=True, max_length=20, null=True)),
                ('cellphone_no', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('max_load', models.IntegerField(blank=True, null=True)),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationStaffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('stafff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStaff',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=255)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackStaffs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs')),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('student_number', models.CharField(blank=True, editable=False, max_length=12, null=True, unique=True)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('suffix', models.CharField(blank=True, max_length=20, null=True)),
                ('nickname', models.CharField(blank=True, max_length=50, null=True)),
                ('dob', models.DateField(blank=True, null=True)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('pob', models.CharField(blank=True, max_length=100, null=True)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('address', models.TextField()),
                ('nationality', models.CharField(blank=True, max_length=50, null=True)),
                ('religion', models.CharField(blank=True, max_length=50, null=True)),
                ('rank_in_family', models.IntegerField(blank=True, null=True)),
                ('telephone_nos', models.CharField(blank=True, max_length=20, null=True)),
                ('mobile_phone_nos', models.CharField(blank=True, max_length=20, null=True)),
                ('is_covid_vaccinated', models.BooleanField(default=False)),
                ('date_of_vaccination', models.DateField(blank=True, null=True)),
                ('student_status', models.CharField(blank=True, max_length=255, null=True)),
                ('profile_pic', models.FileField(blank=True, null=True, upload_to='profile_pics/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('GradeLevel_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.gradelevel')),
                ('admin', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('session_year_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.sessionyearmodel')),
            ],
        ),
        migrations.CreateModel(
            name='StudentPromotionHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_date', models.DateField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('new_grade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='new_grade', to='student_management_app.gradelevel')),
                ('previous_grade', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_grade', to='student_management_app.gradelevel')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='PreviousSchool',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_school_name', models.CharField(blank=True, max_length=100, null=True)),
                ('previous_school_address', models.CharField(blank=True, max_length=255, null=True)),
                ('previous_grade_level', models.CharField(blank=True, max_length=20, null=True)),
                ('previous_school_year_attended', models.CharField(blank=True, max_length=255, null=True)),
                ('previous_teacher_name', models.CharField(blank=True, max_length=100, null=True)),
                ('students_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='ParentGuardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(blank=True, max_length=100, null=True)),
                ('father_occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('guardian_name', models.CharField(blank=True, max_length=100, null=True)),
                ('guardian_occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('students_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='NotificationStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveReportStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_date', models.CharField(max_length=255)),
                ('leave_message', models.TextField()),
                ('leave_status', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackStudent',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('feedback', models.TextField()),
                ('feedback_reply', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
        migrations.AddField(
            model_name='enrollment',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students'),
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emergency_contact_name', models.CharField(blank=True, max_length=100, null=True)),
                ('emergency_contact_relationship', models.CharField(blank=True, max_length=50, null=True)),
                ('emergency_contact_address', models.CharField(blank=True, max_length=255, null=True)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('emergency_enrolling_teacher', models.CharField(blank=True, max_length=100, null=True)),
                ('emergency_referred_by', models.CharField(blank=True, max_length=100, null=True)),
                ('emergency_date', models.DateField(blank=True, null=True)),
                ('students_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('attendance_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.attendance')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student_management_app.students')),
            ],
        ),
        migrations.AddField(
            model_name='assignsection',
            name='Student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students'),
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_name', models.CharField(blank=True, max_length=255, null=True)),
                ('subject_description', models.CharField(blank=True, max_length=255, null=True)),
                ('subject_code', models.CharField(blank=True, max_length=255, null=True)),
                ('subject_hours', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('GradeLevel_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.gradelevel')),
                ('curriculum_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.curriculums')),
            ],
        ),
        migrations.CreateModel(
            name='StudentResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subject_first_quarter', models.FloatField(default=0)),
                ('subject_second_quarter', models.FloatField(default=0)),
                ('subject_third_quarter', models.FloatField(default=0)),
                ('subject_fourth_quarter', models.FloatField(default=0)),
                ('subject_final_grade', models.FloatField(default=0)),
                ('subject_exam_marks', models.FloatField(default=0)),
                ('subject_assignment_marks', models.FloatField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.subjects')),
            ],
        ),
        migrations.AddField(
            model_name='load',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.subjects'),
        ),
        migrations.AddField(
            model_name='attendance',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='student_management_app.subjects'),
        ),
    ]