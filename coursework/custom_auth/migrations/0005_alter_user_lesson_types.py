# Generated by Django 4.2.7 on 2024-06-07 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0004_user_lesson_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='lesson_types',
            field=models.TextField(default='Лабораторное занятие - 0xffFFE2B5\nПрактическое занятие - 0xff00a2ff', verbose_name='Типы занятий (Название~цвет)'),
        ),
    ]
