# Generated by Django 4.2.3 on 2023-07-27 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_step_assigned_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='assigned_to',
            field=models.CharField(max_length=100),
        ),
    ]