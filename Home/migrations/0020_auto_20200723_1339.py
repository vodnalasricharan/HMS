# Generated by Django 3.0.8 on 2020-07-23 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0019_auto_20200723_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='appeal',
            name='in_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='appeal',
            name='out_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='appeal',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('used', 'Used')], default='pending', max_length=200, null=True),
        ),
    ]
