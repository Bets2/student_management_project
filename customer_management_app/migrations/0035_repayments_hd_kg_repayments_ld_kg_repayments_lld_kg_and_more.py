# Generated by Django 4.0.5 on 2023-02-03 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_management_app', '0034_disbursements_contract_monthly_target_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='repayments',
            name='hd_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='repayments',
            name='ld_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='repayments',
            name='lld_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='repayments',
            name='other_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='repayments',
            name='pet_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='repayments',
            name='pp_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='repayments',
            name='ps_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='repayments',
            name='pvc_kg',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
