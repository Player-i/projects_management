# Generated by Django 4.2.4 on 2024-01-21 19:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_myuser_progress_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='step',
            name='name',
        ),
    ]
