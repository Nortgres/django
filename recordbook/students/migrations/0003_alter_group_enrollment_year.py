# Generated by Django 5.0.1 on 2024-01-22 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_group_student_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='enrollment_year',
            field=models.IntegerField(verbose_name='Год зачисления'),
        ),
    ]
