# Generated by Django 4.2.4 on 2024-01-20 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_alter_project_due_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='due_date',
            new_name='todays_date',
        ),
        migrations.RenameField(
            model_name='step',
            old_name='due_date',
            new_name='todays_date',
        ),
    ]