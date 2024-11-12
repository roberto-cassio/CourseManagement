from rest_framework import serializers
from coursemanagement.models.classes import Classes

class ClassesSerializer(serializers.ModelSerializer):
    duration = serializers.DurationField(
        help_text="Formato: 'DD HH:MM:SS'. Exemplo: '01 12:30:00' para 1 dia, 12 horas e 30 minutos."
    )
    class Meta:
        model = Classes
        fields = ['id', 'name', 'topic', 'date', 'courses', 'duration']
        
    '''Para garantir que o método clean seja chamado no Model'''
    def validate(self,data):
        instance = Classes(**data)
        instance.clean()
        return data