# Generated by Django 3.0.8 on 2020-07-22 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0006_auto_20200722_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.CharField(blank=True, choices=[('CSE', 'CSE'), ('IT', 'IT'), ('EEE', 'EEE'), ('MECH', 'MECH'), ('ECE', 'ECE')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='rollno',
            field=models.CharField(blank=True, max_length=200, primary_key=True, serialize=False),
        ),
    ]
