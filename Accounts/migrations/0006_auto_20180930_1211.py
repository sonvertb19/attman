# Generated by Django 2.1.1 on 2018-09-30 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_auto_20180930_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetable',
            name='period',
            field=models.IntegerField(null=True),
        ),
    ]
