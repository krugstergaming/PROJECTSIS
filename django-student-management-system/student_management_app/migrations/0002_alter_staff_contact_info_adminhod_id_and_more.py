# Generated by Django 5.1 on 2024-11-27 06:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff_contact_info',
            name='adminhod_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.adminhod'),
        ),
        migrations.AlterField(
            model_name='staff_contact_info',
            name='staffs_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs'),
        ),
        migrations.AlterField(
            model_name='staff_employment_info',
            name='adminhod_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.adminhod'),
        ),
        migrations.AlterField(
            model_name='staff_employment_info',
            name='staffs_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs'),
        ),
        migrations.AlterField(
            model_name='staff_government_id_info',
            name='adminhod_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.adminhod'),
        ),
        migrations.AlterField(
            model_name='staff_government_id_info',
            name='staffs_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs'),
        ),
        migrations.AlterField(
            model_name='staff_physical_info',
            name='adminhod_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.adminhod'),
        ),
        migrations.AlterField(
            model_name='staff_physical_info',
            name='staffs_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs'),
        ),
        migrations.AlterField(
            model_name='staffs_educ_background',
            name='adminhod_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.adminhod'),
        ),
        migrations.AlterField(
            model_name='staffs_educ_background',
            name='staffs_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.staffs'),
        ),
    ]
