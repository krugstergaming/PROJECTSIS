# Generated by Django 5.1 on 2024-10-27 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0002_rename_remarks_balancepayment_payment_balance_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balancepayment',
            name='payment_balance_remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]