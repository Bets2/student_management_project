# Generated by Django 4.0.5 on 2023-01-15 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_management_app', '0032_alter_grantmanagement_monthly_volume_report_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repayments',
            name='repayment_type',
        ),
    ]
