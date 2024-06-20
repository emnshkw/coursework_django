from rest_framework import serializers
from .models import LessonModel

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonModel
        fields = '__all__'
