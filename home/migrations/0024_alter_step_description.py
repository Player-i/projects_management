# Generated by Django 4.2.4 on 2024-01-21 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_step_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
