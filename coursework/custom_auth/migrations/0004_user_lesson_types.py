# Generated by Django 4.2.7 on 2024-06-07 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_remove_user_city_remove_user_history_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lesson_types',
            field=models.TextField(default='\n    Лабораторное занятие - 0xffFFE2B5\n\n    Практическое занятие - 0xff00a2ff\n    ', verbose_name='Типы занятий (Название~цвет)'),
        ),
    ]
