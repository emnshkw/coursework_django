# Generated by Django 4.2.7 on 2024-06-07 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultmodel',
            name='lesson_name',
        ),
        migrations.AddField(
            model_name='resultmodel',
            name='lesson_id',
            field=models.IntegerField(default=0, verbose_name='ID предмета'),
        ),
        migrations.AlterField(
            model_name='resultmodel',
            name='result_group',
            field=models.IntegerField(default=0, verbose_name='ID группы'),
        ),
    ]
