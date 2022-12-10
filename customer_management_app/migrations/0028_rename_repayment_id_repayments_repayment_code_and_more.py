# Generated by Django 4.0.5 on 2022-12-10 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_management_app', '0027_rename_actual_tonnage_repayments_actual_volume_tone_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='repayments',
            old_name='repayment_id',
            new_name='repayment_code',
        ),
        migrations.AddField(
            model_name='repayments',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
