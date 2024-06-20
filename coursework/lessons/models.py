from django.db import models
from custom_auth.models import User

class LessonModel (models.Model):
    lesson_title = models.TextField('Название занятия',default='')
    lesson_type = models.TextField('Тип занятия~Hex цвет',default='')
    place = models.TextField('Аудитория',blank=True)
    group_id = models.IntegerField('ID группы',default=0)
    group_name = models.TextField('Название группы',default='')
    group_number = models.TextField('Номер группы', default='')
    group_info = models.TextField('Информация о группе (ФИО-Присутствие-Оценка-Примечание)',default='')
    teacher_id = models.IntegerField('ID учителя',default=0)
    date = models.TextField('Дата занятия',default='')

    def __str__(self):
        try:
            teacher = User.objects.get(id=self.teacher_id)
            return f'Название занятия - {self.lesson_title}. Преподаватель - {teacher.username}. Дата проведения - {self.date}'
        except:
            return f'Номер занятия - {self.lesson_title}. Преподаватель указан неверно.'

    class Meta:
        verbose_name = 'Занятие'
        verbose_name_plural = "Занятия"