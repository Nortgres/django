# Generated by Django 5.0.1 on 2024-01-22 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5, verbose_name='Группа')),
                ('course', models.CharField(max_length=2, verbose_name='Курс')),
                ('enrollment_year', models.ImageField(upload_to='', verbose_name='Год зачисления')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.group', verbose_name='Группа'),
        ),
    ]