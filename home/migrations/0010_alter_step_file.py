# Generated by Django 4.2.3 on 2023-08-02 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_step_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='static/files/'),
        ),
    ]
