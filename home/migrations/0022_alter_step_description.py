# Generated by Django 4.2.4 on 2024-01-21 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_step_file2_step_file3_step_file4'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
