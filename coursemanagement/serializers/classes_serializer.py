from rest_framework import serializers
from coursemanagement.models.classes import Classes

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = ['name', 'topic', 'date', 'courses']