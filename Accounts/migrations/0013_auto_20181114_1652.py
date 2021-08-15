# Generated by Django 2.1.3 on 2018-11-14 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0012_attendance_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='value_int',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='attendance',
            name='value_str',
            field=models.CharField(default='Not Marked', max_length=10),
        ),
    ]
