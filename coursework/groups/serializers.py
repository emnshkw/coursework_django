from rest_framework import serializers
from .models import GroupModel

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = '__all__'
