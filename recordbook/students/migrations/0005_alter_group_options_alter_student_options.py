# Generated by Django 5.0.1 on 2024-01-25 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_alter_student_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'Студент', 'verbose_name_plural': 'Студенты'},
        ),
    ]