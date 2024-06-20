from django.db import models
from lessons.models import LessonModel
from custom_auth.models import User


class ResultModel(models.Model):
    result_group = models.IntegerField('ID группы',default=0)
    teacher_id = models.IntegerField('ID преподавателя',default='')
    lesson_title = models.TextField('Название предмета',default='')
    result = models.TextField('Итоговая сводка',default='')
    result_points = models.TextField('Итоговые оценки',default='')
    def __str__(self):
        teacher = User.objects.get(pk=self.teacher_id)
        return f'Название предмета - {self.lesson_title}. Преподаватель - {teacher.username}'

    class Meta:
        verbose_name = 'Сводка оценок'
        verbose_name_plural = "Сводки оценок"
