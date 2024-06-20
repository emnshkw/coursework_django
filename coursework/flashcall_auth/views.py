import datetime

from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Flashcall_model
import requests
from custom_auth.models import User
# Create your views here.

def send_code(phone):
    request_data = {
        "public_key": '3d7ab9ff70eed918ee02b0f983c73a3b',
        'phone': str(phone).replace('+',''),
        'campaign_id': '1724016472'
    }
    url = f'https://zvonok.com/manager/cabapi_external/api/v1/phones/flashcall/?public_key={request_data["public_key"]}&phone={request_data["phone"]}&campaign_id={request_data["campaign_id"]}'
    response = requests.request('POST', url)
    return response.json()

def create_token(phone,password):
    request_data = {
        "phone":phone,
        "password":password
    }
    url = f'http://127.0.0.1:80/auth/token/login'
    response = requests.request('POST', url,data=request_data)
    return response.json()


class Flashcall_get(APIView):
    permission_classes = (AllowAny,)
    def post(self,request, *args, **kwargs):
        data = request.data

        try:
            user = User.objects.get(phone=data['phone'])
            if user.is_active:
                return Response({'status':'Failed','message':'Пользователь уже существует'})
            else:
                user.delete()
        except:
            pass

        try:
            if data['phone'] is not None and data['username'] is not None:
                pass
            else:
                return Response({'status':'Failed','message':"Что-то пошло не так!"})
        except:
            return Response({'status':'Failed','message':"Что-то пошло не так!"})
        try:
            model = Flashcall_model.objects.get(phone_number=data['phone'])
            old_date = datetime.datetime.strptime(model.date, '%m/%d/%y %H:%M')
            time_delta = (datetime.datetime.now() - old_date).seconds
            if model.attempts % 10 == 0:
                return Response({"status": "Failed", 'message': f"Попробуйте через {(3600-time_delta)//60} минут {(3600-time_delta)%60} секунд (ы)"})
            if model.attempts % 3 == 0 and model.attempts != 0 and time_delta < 60:
                return Response({"status":"Failed",'message':f"Попробуйте через {60 - time_delta} секунд (ы)"})
            else:
                response = send_code(data['phone'])
                response_data = response['data']
                if response['status'] == 'ok':
                    model.code = response_data['pincode']
                    model.date = str(datetime.datetime.now().strftime("%m/%d/%y %H:%M"))
                    model.attempts += 1
                    model.save()
                    return Response({'status':'Success','message':"Звонок-сброс был отправлен!"})
        except:
            if len(data['phone'].replace('+','')) == 11:
                response = send_code(data['phone'])
                response_data = response['data']
                if response['status'] == 'ok':
                    Flashcall_model.objects.create(name=data['username'],phone_number=data['phone'],code=response_data['pincode'],date=str(datetime.datetime.now().strftime("%m/%d/%y %H:%M")),attempts=1)
                    return Response({'status':'Success','message':"Звонок-сброс был отправлен!"})
            else:
                return Response({'status':'Failed','message':'Введён неверный номер телефона'})

        return Response({'status':'Failed','message':'Что-то пошло не так'})


class Flashcall_check(APIView):
    permission_classes = (AllowAny,)
    def post(self,request, *args, **kwargs):
        data = request.data
        try:
            user = User.objects.get(phone=data['phone'])
            return Response({'status':'Failed','message':"Пользователь уже существует."})
        except:
            pass
        if len(data['phone'].replace('+','')) == 11 and len(data['code']) == 4:
            try:
                code_check = int(data['code'])
            except:
                return Response({'status':'Failed','message':'Код должен состоять из чисел'})
        try:
            user_code_model = Flashcall_model.objects.get(phone_number=data['phone'])
            user_code = user_code_model.code
            code_to_check = data['code']
            if user_code == code_to_check:
                try:
                    username = data['username']
                    password = data['password']
                    re_password = data['re_password']
                    phone = data['phone']
                    if password == re_password:
                        User.objects.create_user(username,phone,password)
                        new_user = User.objects.get(phone = phone)
                        new_user.activate()
                        user_code_model.change_activate()
                        token = create_token(phone,password)['auth_token']
                        return Response({'status': 'Success', 'message': token})
                    else:
                        return Response({'status': 'Failed', 'message': 'Пароли не совпадают'})
                except Exception as e:
                    print(e)
                    return Response({'status':'Failed','message':'Не указано одно из обязательных полей'})
            else:
                return Response({'status':'Failed','message':'Проверочный код не подходит.'})
        except:
            return Response({'status':'Failed','message':'Что-то пошло не так!'})


class Flashcall_get_reset_password(APIView):
    permission_classes = (AllowAny,)
    def post(self,request, *args, **kwargs):
        data = request.data
        try:
            user = User.objects.get(phone=data['phone'])
            model = Flashcall_model.objects.get(phone_number=data['phone'])
            old_date = datetime.datetime.strptime(model.date, '%m/%d/%y %H:%M')
            time_delta = (datetime.datetime.now() - old_date).seconds
            if model.attempts % 10 == 0 and (3600 - time_delta) > 0:
                return Response({"status": "Failed",
                                 'message': f"Попробуйте через {(3600 - time_delta) // 60} минут {(3600 - time_delta) % 60} секунд (ы)"})
            elif model.attempts % 3 == 0 and model.attempts != 0 and time_delta < 60:
                return Response({"status": "Failed", 'message': f"Попробуйте через {60 - time_delta} секунд (ы)"})
            else:
                response = send_code(data['phone'])
                response_data = response['data']
                if response['status'] == 'ok':
                    model.code = response_data['pincode']
                    model.date = str(datetime.datetime.now().strftime("%m/%d/%y %H:%M"))
                    model.activated = False
                    model.attempts += 1
                    model.save()
                    return Response({'status': 'Success', 'message': "Звонок-сброс был отправлен!"})
                return Response({'status':"success",'message':'Что-то пошло не так!'})
        except:
            return Response({"status":"Failed",'message':"Пользователь не найден."})

class Flashcall_check_reset_password(APIView):
    permission_classes = (AllowAny,)
    def post(self,request, *args, **kwargs):
        data = request.data
        # try:
        user = User.objects.get(phone=data['phone'])
        model = Flashcall_model.objects.get(phone_number=data['phone'])
        if model.activated:
            return Response({'status':'failed','message':'Запросите новый код.'})
        if data['code'] == model.code:
            user.set_password(data['password'])
            model.change_activate()
            user.save()
            return Response({'status': 'Success', 'message': create_token(data['phone'],data['password'])})
        else:
            return Response({'status':"failed",'message':'Что-то пошло не так!'})
        # except:
        #     return Response({"status":"Failed",'message':"Что-то пошло не так!"})
