from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User

# Create your views here.
class UserView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            curr_user = request.user
            return Response({'status': 'success','username': curr_user.username,
                             'id': curr_user.id, 'phone': str(curr_user.phone),'lesson_types':curr_user.lesson_types,'lesson_names':curr_user.lesson_names})
        except:
            return Response({'status': 'failed', 'message': "пользователь не найден"})
    def post(self,request,*args,**kwargs):
        try:
            curr_user = request.user
            lesson_type = request.data.get('lesson_type')
            color = request.data.get('color')
            if not lesson_type:
                return Response({'status':'failed','message':"Укажите название типа занятия"})
            if not color:
                return Response({'status':'failed','message':"Укажите цвет типа занятия"})
            curr_user.add_lesson_type(f'{lesson_type}~{color}')
            return Response({'status': 'success','message':'Тип занятий успешно добавлен'})
        except Exception as e:
            print(e)
            return Response({'status': 'failed', 'message': "пользователь не найден"})
    def put(self,request,*args,**kwargs):
        try:
            curr_user = request.user
        except Exception as e:
            return Response({'status': 'failed', 'message': "пользователь не найден"})
        lesson_name = request.data.get('lesson_name')
        if not lesson_name:
            return Response({'status':'failed','message':"Укажите название занятия"})
        curr_user.add_lesson_name(lesson_name)
        return Response({'status': 'success','message':'Занятие успешно добавлено'})

    def delete(self,request,*args,**kwargs):
        try:
            curr_user = request.user
        except Exception as e:
            return Response({'status': 'failed', 'message': "пользователь не найден"})
        lesson_type = request.data.get('lesson_type')
        color = request.data.get('color')
        if lesson_type and color:
            curr_user.remove_lesson_type(f"{lesson_type}~{color}")
            return Response({'status':'success','message':"Тип занятия был удалён"})
        lesson_name = request.data.get('lesson_name')
        if lesson_name:
            curr_user.remove_lesson_name(lesson_name)
            return Response({'status': 'success', 'message': "Занятие было удалёно"})
        return Response({'status':'failed','message':"Укажите то, что вам нужно удалить"})