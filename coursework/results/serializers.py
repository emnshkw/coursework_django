from rest_framework import serializers
from .models import ResultModel

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultModel
        fields = '__all__'
