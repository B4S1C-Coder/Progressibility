# Generated by Django 4.1.4 on 2023-07-10 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress_tracker', '0004_alter_progressibilitytask_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressibilitytask',
            name='completed',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='completed'),
        ),
        migrations.AlterField(
            model_name='progressibilitytask',
            name='dateadded',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='date added'),
        ),
    ]
