# Generated by Django 4.2.7 on 2024-06-16 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0007_remove_user_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lesson_names',
            field=models.TextField(blank=True, verbose_name='Названия занятий'),
        ),
    ]
