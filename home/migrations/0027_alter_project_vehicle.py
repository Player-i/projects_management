# Generated by Django 4.2.4 on 2024-05-22 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_step_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='vehicle',
            field=models.TextField(blank=True, null=True),
        ),
    ]