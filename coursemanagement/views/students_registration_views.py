from ..models.students_registration import StudentRegistration
from coursemanagement.serializers.students_registration_serializer import StudentRegistrationSerializer
from coursemanagement.serializers.studentes_unregister_serializer import StudentUnregisterSerializer
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
    
    '''
    Método para Cancelamento de Matrícula
    '''
    @action(detail=False, methods=['post'], serializer_class=StudentUnregisterSerializer)
    def cancel(self, request):
        serializer = StudentUnregisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": "Dados inválidos", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        student_id = request.data.get('student')
        course_id = request.data.get('courses')

        
        try:
            canceled_registration = cancel_registration(student_id, course_id)
            return Response({"message": "Matrícula cancelada com Sucesso!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Erro inesperado", "details": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)



