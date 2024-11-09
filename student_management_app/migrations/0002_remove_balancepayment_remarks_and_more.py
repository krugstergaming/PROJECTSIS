# Generated by Django 5.1 on 2024-11-01 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balancepayment',
            name='remarks',
        ),
        migrations.AddField(
            model_name='balancepayment',
            name='payment_balance_remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sessionyearmodel',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]