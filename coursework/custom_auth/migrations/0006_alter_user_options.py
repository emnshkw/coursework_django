# Generated by Django 4.2.7 on 2024-06-07 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0005_alter_user_lesson_types'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Преподаватель', 'verbose_name_plural': 'Преподаватели'},
        ),
    ]
