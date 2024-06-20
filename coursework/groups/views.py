from rest_framework.views import APIView
from rest_framework.response import Response
from .models import GroupModel
from .serializers import GroupSerializer

def get_groups(teacher_id):
    all_groups = GroupModel.objects.all()
    teacher_groups = []
    for group in all_groups:
        if group.teacher_id == teacher_id:
            teacher_groups.append(group)
    return teacher_groups

class GroupAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        teacher = request.user
        groups = get_groups(teacher.id)
        if len(groups) == 0:
            return Response({'status':'failed','message':'У вас ещё нет групп. Создайте'})
        if not pk:
            # lst = GroupModel.objects.all().values()
            data = GroupSerializer(groups, many=True).data
            return Response({'status':'success','groups':data})
        else:
            group = [i for i in groups if i.id == pk]
            data = GroupSerializer(group, many=True).data
            return Response({'status':'success','group':data})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            return Response({'status':'failed','message':'Метод POST запрещён.'})
        teacher = request.user
        group_name = request.data.get('group_name')
        if not group_name:
            group_name = ''
        group_number = request.data.get('group_number')
        if not group_number:
            return Response({'status': 'failed', 'message': 'Укажите номер группы'})
        marks = request.data.get('marks')
        if not marks:
            marks = ''
        students = request.data.get('students')
        if not students:
            return Response({'status': 'failed', 'message': 'Укажите студентов в группе'})

        GroupModel.objects.create(group_name=group_name,group_number=group_number,marks=marks,students=students,teacher_id=teacher.id)
        return Response({'status': 'success', 'message': 'Группа успешно добавлена!'})
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'status':'failed','message':'Метод PUT запрещён.'})
        teacher = request.user
        try:
            group = GroupModel.objects.get(pk=pk)
        except:
            return Response({'status': 'failed', 'message': "Указанная группа не существует."})
        if group.teacher_id != teacher.id:
            return Response({'status':'failed','message':"Указанная группа не принадлежит вам."})
        group_name = request.data.get('group_name')
        if group_name:
            group.group_name = group_name
        group_number = request.data.get('group_number')
        if group_number:
            group.group_number = group_number
        marks = request.data.get('marks')
        if marks:
            group.marks = marks
        students = request.data.get('students')
        if students:
            group.students = students
        group.save()
        return Response({'status': 'success', 'message': 'Группа успешно изменена!'})
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({'status':'failed','message':'Метод DELETE запрещён.'})
        teacher = request.user
        try:
            group = GroupModel.objects.get(pk=pk)
        except:
            return Response({'status': 'failed', 'message': "Указанная группа не существует."})
        if group.teacher_id != teacher.id:
            return Response({'status':'failed','message':"Указанная группа не принадлежит вам."})
        else:
            group.delete()
            return Response({'status': 'success', 'message': "Группа успешно удалена!"})