# Generated by Django 4.2.2 on 2023-06-27 09:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0014_project_git_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='first_created',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
