# Generated by Django 4.2.2 on 2023-06-27 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0015_project_first_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='short_description',
        ),
        migrations.AddField(
            model_name='project',
            name='documentation',
            field=models.URLField(default='', max_length=1000),
        ),
    ]