# Generated by Django 4.1.4 on 2023-07-10 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('progress_tracker', '0005_alter_progressibilitytask_completed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='progressibilitytask',
            name='completed',
            field=models.BooleanField(default=False, verbose_name='completed'),
        ),
    ]