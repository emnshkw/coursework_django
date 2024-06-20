# Generated by Django 4.2.7 on 2024-06-07 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupmodel',
            options={'verbose_name': 'Группа', 'verbose_name_plural': 'Группы'},
        ),
        migrations.AddField(
            model_name='groupmodel',
            name='teacher_id',
            field=models.IntegerField(default=0, verbose_name='ID преподавателя'),
        ),
    ]