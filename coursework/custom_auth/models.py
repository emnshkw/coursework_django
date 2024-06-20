from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('Имя', max_length=255)
    phone = PhoneNumberField('Номер телефона',unique=True,region='RU')
    lesson_types = models.TextField('Типы занятий (Название~цвет)',default='Лабораторное занятие - 0xffFFE2B5\nПрактическое занятие - 0xff00a2ff')
    lesson_names = models.TextField('Названия занятий',blank=True)
    date_joined = models.DateTimeField('Дата последнего входа', auto_now_add=True)
    is_active = models.BooleanField('Пользователь подтверждён', default=False)
    is_staff = models.BooleanField('Является сотрудником',default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']


    def activate(self):
        self.is_active = True
        self.save()
    def __str__(self):
        return str(self.phone)

    def add_lesson_type(self,new):
        types = [i for i in self.lesson_types.split('\n') if i != '']
        types.append(new)
        self.lesson_types = '\n'.join(types)
        self.save()
    def add_lesson_name(self,new):
        names = [i for i in self.lesson_names.split('\n') if i != '']
        names.append(new)
        self.lesson_names = '\n'.join(names)
        self.save()
    def remove_lesson_type(self,toDel):
        types = [i for i in self.lesson_types.split('\n') if i != '']
        types.remove(toDel)
        self.lesson_types = '\n'.join(types)
        self.save()

    def remove_lesson_name(self,toDel):
        names = [i for i in self.lesson_names.split('\n') if i != '']
        names.remove(toDel)
        self.lesson_names = '\n'.join(names)
        self.save()
    class Meta:
        verbose_name = ('Преподаватель')
        verbose_name_plural = ('Преподаватели')
