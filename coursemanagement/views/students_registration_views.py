from ..models.students_registration import StudentRegistration
from coursemanagement.serializers.students_registration_serializer import StudentRegistrationSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from coursemanagement.services.enrollment_service import enroll_student, cancel_registration
from coursemanagement.models.students import Student
from coursemanagement.models.courses import Courses


class StudentRegistrationViewSet(viewsets.ModelViewSet):
    queryset = StudentRegistration.objects.all()
    serializer_class = StudentRegistrationSerializer


    def create(self,request, *args, **kwargs):
        student_id = request.data.get('student')
        course_id = request.data.get('courses')
        enrollment_date = request.data.get('enrollment_date')
        cancellation_date = request.data.get("cancellation_date")

        try:
            student = Student.objects.get(id=student_id)
            course = Courses.objects.get(id=course_id)

            registration = enroll_student(student, course, enrollment_date, cancellation_date)
            return Response({"message": "Aluno matriculado com sucesso!"}, status=status.HTTP_201_CREATED)
        except Student.DoesNotExist:
            return Response({"error": "Aluno não encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Courses.DoesNotExist:
            return Response({"error": "Curso não encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, id=None):
        student_name = request.data.get('student_name')
        course_title = request.data.get('course_title')

        if not student_name or not course_title:
            return Response({"error": "Nome do Aluno e do Curso são obrigatórios."})
        
        try:
            canceled_registration = cancel_registration(student_name, course_title)
            return Response({"message": "Matrícula cancelada com Sucesso!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Erro inesperado"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)



