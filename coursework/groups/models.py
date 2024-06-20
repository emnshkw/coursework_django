from django.db import models
from custom_auth.models import User

class GroupModel (models.Model):
    group_number = models.TextField('Номер группы',default='')
    group_name = models.TextField('Название группы',blank=True)
    marks = models.TextField('Примечание к группе',blank=True)
    students = models.TextField('Состав группы',default='')
    teacher_id = models.IntegerField('ID преподавателя',default=0)

    def __str__(self):
        try:
            teacher = User.objects.get(id=self.teacher_id)
            return f'Номер группы - {self.group_number}. Преподаватель - {teacher.username}'
        except:
            return f'Номер группы - {self.group_number}. Преподаватель указан неверно.'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'