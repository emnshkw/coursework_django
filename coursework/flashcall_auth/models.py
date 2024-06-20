from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Flashcall_model(models.Model):
    phone_number = PhoneNumberField('Номер телефона',unique=True,region='RU')
    name = models.TextField('Имя пользователя')
    code = models.TextField('Отправленный код подтверждения')
    date = models.TextField('Когда был запрошен код')
    activated = models.BooleanField('Код был введён',default=False)
    attempts = models.IntegerField('Количество попыток',default=0)
    def __str__(self):
        return f'Номер телефона - {self.phone_number}, имя - {self.name}, код - {self.code}, запрошен - {self.date}'

    def change_activate(self):
        self.activated = not(self.activated)
        self.save()

    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'

