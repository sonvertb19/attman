# Generated by Django 2.1.1 on 2018-09-29 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_delete_abc'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetable',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.Subject'),
        ),
    ]