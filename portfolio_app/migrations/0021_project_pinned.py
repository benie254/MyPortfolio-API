# Generated by Django 4.2.2 on 2023-06-27 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0020_project_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='pinned',
            field=models.CharField(blank=True, choices=[('pinned', 'pinned'), ('unpinned', 'unpinned')], max_length=500, null=True),
        ),
    ]
