# Generated by Django 5.0.1 on 2024-01-25 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0006_student_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='slug',
            field=models.SlugField(max_length=255, unique=True, verbose_name='URL'),
        ),
    ]