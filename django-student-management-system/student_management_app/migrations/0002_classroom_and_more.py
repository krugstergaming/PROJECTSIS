# Generated by Django 5.1 on 2024-12-09 13:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('classroom_name', models.CharField(max_length=255)),
                ('status', models.CharField(blank=True, choices=[('Available', 'Available'), ('Taken', 'Taken')], max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='staff_contact_info',
            old_name='emergency_contact',
            new_name='emergency_contact_name',
        ),
        migrations.RemoveField(
            model_name='balancepayment',
            name='remarks',
        ),
        migrations.RemoveField(
            model_name='studentresult',
            name='subject_assignment_marks',
        ),
        migrations.RemoveField(
            model_name='studentresult',
            name='subject_exam_marks',
        ),
        migrations.AddField(
            model_name='adminhod',
            name='max_load',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='balancepayment',
            name='payment_balance_remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='failed_login_attempts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_login_session_key',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='session_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
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
        migrations.AddField(
            model_name='staff_contact_info',
            name='adminhod_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.adminhod'),
        ),
        migrations.AddField(
            model_name='staff_contact_info',
            name='emergency_contact_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='staff_employment_info',
            name='adminhod_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.adminhod'),
        ),
        migrations.AddField(
            model_name='staff_government_id_info',
            name='adminhod_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.adminhod'),
        ),
        migrations.AddField(
            model_name='staff_physical_info',
            name='adminhod_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.adminhod'),
        ),
        migrations.AddField(
            model_name='staffs_educ_background',
            name='adminhod_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.adminhod'),
        ),
        migrations.AddField(
            model_name='studentresult',
            name='remarks',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='staff_contact_info',
            name='staffs_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs'),
        ),
        migrations.AlterField(
            model_name='staff_employment_info',
            name='position',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='staff_employment_info',
            name='staffs_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs'),
        ),
        migrations.AlterField(
            model_name='staff_government_id_info',
            name='staffs_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs'),
        ),
        migrations.AlterField(
            model_name='staff_physical_info',
            name='height',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='staff_physical_info',
            name='staffs_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs'),
        ),
        migrations.AlterField(
            model_name='staff_physical_info',
            name='weight',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='staffs',
            name='citizenship',
            field=models.CharField(blank=True, default='Filipino', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='staffs_educ_background',
            name='staffs_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs'),
        ),
    ]
