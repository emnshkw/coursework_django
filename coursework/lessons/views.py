from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LessonModel
from .serializers import LessonSerializer
from groups.views import get_groups

from datetime import datetime
def get_lessons(teacher_id):
    all_lessons = LessonModel.objects.all()
    teacher_lessons = []
    for lesson in all_lessons:
        if lesson.teacher_id == teacher_id:
            teacher_lessons.append(lesson)
    data = LessonSerializer(teacher_lessons, many=True).data
    for i in range(len(teacher_lessons)):
        for x in range(i + 1, len(teacher_lessons)):
            first = teacher_lessons[i]
            second = teacher_lessons[x]
            first_date_str = first.date.split(' ')[0].split('.')
            first_time_str = first.date.split(' ')[1].split('-')[0].split(':')
            first_date = datetime(int(first_date_str[2]), int(first_date_str[1]), int(first_date_str[0]),
                                  int(first_time_str[0]), int(first_time_str[1]))
            second_date_str = second.date.split(' ')[0].split('.')
            second_time_str = second.date.split(' ')[1].split('-')[0].split(':')
            second_date = datetime(int(second_date_str[2]), int(second_date_str[1]), int(second_date_str[0]),
                                   int(second_time_str[0]), int(second_time_str[1]))
            if second_date < first_date:
                teacher_lessons[i] = second
                teacher_lessons[x] = first
    return teacher_lessons

class LessonAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        teacher = request.user
        lessons = get_lessons(teacher.id)
        if len(lessons) == 0:
            return Response({'status':'failed','message':'У вас ещё нет занятий. Создайте'})
        if not pk:
            # lst = LessonModel.objects.all().values()
            data = LessonSerializer(lessons, many=True).data
            return Response({'status':'success','lessons':data})
        else:
            lesson = [i for i in lessons if i.id == pk]
            data = LessonSerializer(lesson, many=True).data
            return Response({'status':'success','lesson':data})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return Response({'status':'failed','message':'Метод POST запрещён.'})
        teacher = request.user
        lesson_title = request.data.get('lesson_title')
        if not lesson_title:
            return Response({'status':'failed','message':'Укажите значение поля "Название занятия"'})
        place = request.data.get('place')
        if not place:
            place = ''
        group_id = request.data.get('group_id')
        if not group_id:
            return Response({'status':'failed','message':'Укажите значение поля "Номер группы"'})
        date = request.data.get('date')
        if not date:
            return Response({'status':'failed','message':'Укажите значение поля "Дата занятия"'})
        lesson_type = request.data.get('lesson_type')
        if not lesson_type:
            return Response({'status': 'failed', 'message': 'Укажите значение поля "Тип занятия"'})
        groups = get_groups(teacher.id)
        print(groups)
        choosed_group = [i for i in groups if i.id == group_id]
        if len(choosed_group) == 0:
            return Response({'status': 'failed', 'message': 'Указанной группы не существует'})
        choosed_group = choosed_group[0]
        group_info = ''
        for student in choosed_group.students.split('\n'):
            student = student.replace("\r","")
            group_info += f'{student}~~~\n'
        group_info = '\n'.join([i for i in group_info.split('\n') if i != ''])
        LessonModel.objects.create(lesson_title=lesson_title,place=place,group_id=choosed_group.id,group_info=group_info,teacher_id=teacher.id,date=date,lesson_type=lesson_type,group_name=choosed_group.group_name,group_number=choosed_group.group_number)
        return Response({'status': 'success', 'message': 'Занятие успешно добавлено!'})
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'status':'failed','message':'Метод POST запрещён.'})
        teacher = request.user
        try:
            lesson = LessonModel.objects.get(pk=pk)
        except:
            return Response({'status': 'failed', 'message': "Указанная группа не существует."})
        if lesson.teacher_id != teacher.id:
            return Response({'status':'failed','message':"Указанная группа не принадлежит вам."})
        lesson_title = request.data.get('lesson_title')
        if lesson_title:
            lesson.lesson_title = lesson_title
        place = request.data.get('place')
        if place:
            lesson.place = place
        group_id = request.data.get('group_id')
        if group_id:
            lesson.group_id = group_id
        group_info = request.data.get('group_info')
        if group_info:
            lesson.group_info = group_info
        date = request.data.get('date')
        if date:
            lesson.date = date
        lesson.save()
        return Response({'status': 'success', 'message': 'Информация о занятии успешно изменена!'})
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'status':'failed','message':'Метод POST запрещён.'})
        teacher = request.user
        try:
            lesson = LessonModel.objects.get(pk=pk)
        except:
            return Response({'status': 'failed', 'message': "Указанное занятие не существует."})
        if lesson.teacher_id != teacher.id:
            return Response({'status':'failed','message':"Указанное занятие не принадлежит вам."})
        else:
            lesson.delete()
            return Response({'status': 'success', 'message': "Занятие успешно удалено!"})