# Generated by Django 3.0.8 on 2020-08-01 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0042_auto_20200801_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.CharField(choices=[('I', 'I'), ('II', 'II'), ('III', 'III'), ('IV', 'IV'), ('I-M.tech', 'I-M.tech'), ('II-M.tech', 'II-M.tech')], max_length=200, null=True),
        ),
    ]
