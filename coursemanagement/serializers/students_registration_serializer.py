from rest_framework import serializers
from coursemanagement.models.students_registration import StudentRegistration

'''
Pensei em utilizar serializadores aninhados aqui para facilitar a visualização de dados, já que os Estudantes e Cursos retornam como Id's, de forma a tornar a API
mais intuitiva. Mas considerando que a ideia do projeto é levar em conta também a escalabilidade, isso poderia levar a problemas de perfomance futuros.
Portanto, optei por usar apenas o ID's dos Estudantes e Cursos nas respostas.
'''
class StudentRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentRegistration
        fields = ['id', 'student', 'courses']