# Generated by Django 4.2.7 on 2024-06-16 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_remove_resultmodel_lesson_name_resultmodel_lesson_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultmodel',
            name='result_points',
            field=models.TextField(default='', verbose_name='Итоговые оценки'),
        ),
    ]
