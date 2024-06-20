from django.shortcuts import render
from .models import ResultModel
from rest_framework.views import APIView
from rest_framework.response import Response
from lessons.models import LessonModel
from .serializers import ResultSerializer
from groups.views import get_groups
from lessons.views import get_lessons
from lessons.serializers import LessonSerializer

def get_results(teacher_id):
    all_results = ResultModel.objects.all()
    teacher_results = []
    for result in all_results:
        if result.teacher_id == teacher_id:
            teacher_results.append(result)
    return teacher_results


def get_all_same_lessons(group_id,lesson_title,teacher_id):
    lessons = get_lessons(teacher_id)
    same_lessons = []
    for lesson in lessons:
        if lesson.lesson_title == lesson_title and lesson.group_id == group_id:
            same_lessons.append(lesson)
    return same_lessons


def calculate_result(group,lessons):
    students = {}
    for student in group.students.replace('\r','').split('\n'):
        students[student] = {
            'Посещаемость':0
        }
    for lesson in lessons:
        group_info = lesson.group_info
        lesson_type = lesson.lesson_type.split('~')[0]
        for student_info in group_info.replace('\r','').split('\n'):
            student_info = student_info.split('~')
            fio = student_info[0]
            visited = student_info[1]
            points = student_info[2]
            mark = student_info[3]
            if visited == "+":
                students[fio]['Посещаемость'] += 1
            students[fio][f'{lesson_type}/{lesson.date}'] = points
    return students

def convert_results_to_string(results):
    result_list = []
    cols = ["ФИО","Итог"]
    for student in results.keys():
        res = []
        res.append(student)
        for part_result_key in results[student].keys():
            res.append(results[student][part_result_key])
            if part_result_key not in cols:
                cols.append(part_result_key)
        result_list.append('~'.join([str(i) for i in res]))
    return (cols,result_list)


def get_students_string(result):
    students = []
    for student in result.keys():
        students.append(f'{student}~')
    return '\n'.join(students)


class ResultAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        teacher = request.user
        results = get_results(teacher.id)
        if len(results) == 0:
            return Response({'status':'failed','message':'У вас ещё нет занятий. Создайте'})
        if not pk:
            data = ResultSerializer(results, many=True).data
            return Response({'status':'success','results':data})
        else:
            result = [i for i in results if i.id == pk]
            data = ResultSerializer(result, many=True).data
            return Response({'status':'success','result':data})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        teacher = request.user
        lesson_title = request.data.get('lesson_title')
        if not lesson_title:
            return Response({'status':'failed','message':'Укажите название занятия'})
        group_id = request.data.get('group_id')
        if not group_id:
            return Response({'status':'failed','message':'Укажите ID группы'})
        try:
            group = [i for i in get_groups(teacher.id) if i.id == group_id][0]
        except:
            return Response({'status':'failed','message':'Указанной группы не существует или она не принадлежит вам.'})
        lessons = get_all_same_lessons(group_id, lesson_title, teacher.id)
        results = calculate_result(group, lessons)
        cols,res = convert_results_to_string(results)
        try:
            result = ResultModel.objects.get(pk=pk)
            if result.result_points == '':
                result.result_points = get_students_string(results)
            cols = '~'.join(cols)
            res = '\n'.join(res)
            result.result = f'{cols}\n{res}'
            result.save()
            return Response({'status': 'success', 'message': 'Сводка обновлена.'})
        except:
            cols = '~'.join(cols)
            res = '\n'.join(res)
            result = ResultModel.objects.create(result_group=group_id,teacher_id=teacher.id,result=f'{cols}\n{res}',result_points =get_students_string(results),lesson_title=lesson_title)
            return Response({'status': 'success', 'message': 'Сводка сгенерирована!'})
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'status':'failed','message':'Метод PUT запрещён.'})
        teacher = request.user
        try:
            result = ResultModel.objects.get(pk=pk)
        except:
            return Response({'status': 'failed', 'message': "Указанная группа не существует."})
        if result.teacher_id != teacher.id:
            return Response({'status':'failed','message':"Указанная группа не принадлежит вам."})
        result_group = request.data.get('result')
        if result_group:
            result.result = result_group
        result_points = request.data.get('result_points')
        if result_points:
            result.result_points = result_points
        result.save()
        return Response({'status': 'success', 'message': 'Итоговая сводка успешно изменена!'})
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'status':'failed','message':'Метод POST запрещён.'})
        teacher = request.user
        try:
            result = ResultModel.objects.get(pk=pk)
        except:
            return Response({'status': 'failed', 'message': "Указанная сводка не существует."})
        if result.teacher_id != teacher.id:
            return Response({'status':'failed','message':"Указанная сводка не принадлежит вам."})
        else:
            result.delete()
            return Response({'status': 'success', 'message': "Сводка успешно удалена!"})


class ResultsToGetAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        teacher = request.user
        if not pk:
            lesson_names = teacher.lesson_names.split('\n')
            results = get_results(teacher.id)
            unique_lessons = []
            lessons = get_lessons(teacher.id)
            for lesson in lessons:
                if any(lesson.lesson_title == i.lesson_title and lesson.group_id == i.group_id for i in unique_lessons):
                    continue
                else:
                    unique_lessons.append(lesson)
            data = LessonSerializer(unique_lessons, many=True).data
            for lesson in data:
                if any(i.result_group == lesson['group_id'] and i.lesson_title == lesson['lesson_title'] for i in results):
                    lesson['generated'] = True
                    for i in results:
                        if i.result_group == lesson['group_id'] and i.lesson_title == lesson['lesson_title']:
                            lesson['result_id'] = i.id
                else:
                    lesson['generated'] = False
            return Response({'status':'success','lessons':data})
        else:
            return Response({'status':'failed','message':'Запрет'})
