from rest_framework import serializers
from coursemanagement.models.classes import Classes

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['id', 'name', 'topic', 'date', 'courses', 'duration']
        
    '''Para garantir que o método clean seja chamado no Model'''
    def validate(self,data):
        instance = Classes(**data)
        instance.clean()
        return data