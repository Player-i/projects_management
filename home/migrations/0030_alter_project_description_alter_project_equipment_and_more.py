# Generated by Django 4.2.4 on 2024-05-22 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0029_alter_project_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='equipment',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='vehicle',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
