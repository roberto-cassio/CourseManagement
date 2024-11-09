from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from ..models.students_registration import StudentRegistration
from coursemanagement.serializers.students_registration_serializer import StudentRegistrationSerializer
from coursemanagement.serializers.students_unregister_serializer import StudentUnregisterSerializer
from coursemanagement.services.enrollment_service import enroll_student, cancel_registration
from coursemanagement.models.students import Student
from coursemanagement.models.courses import Courses

'''Como o Registration não tem o SoftDelete, somente data de matrícula e cancelamento(Que faz essencialmente a mesma coisa), o SoftDeleteModelViewSet não é chamado aqui'''
class StudentRegistrationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = StudentRegistration.objects.all()
    serializer_class = StudentRegistrationSerializer
   


    '''O Get só vai buscar alunos com a Matrícula efetivamente ativa ou inativa de acordo com o parâmetro de consulta "status"'''
    def get_queryset(self):
        status_filter = self.request.query_params.get('status', 'active')
        if status_filter == 'active':
            return StudentRegistration.objects.filter(is_active=True)
        if status_filter == 'inactive':
            return StudentRegistration.objects.filter(is_active=False)
        else:
            return StudentRegistration.objects.all()

    '''Matrícula de Criação de Matrícula - Talvez fazer um Serializer somente para o método Get'''

    def create(self,request):
        student_id = request.data.get('student')
        course_id = request.data.get('courses')

        try:
            student = Student.objects.get(id=student_id)
            course = Courses.objects.get(id=course_id)

            registration = enroll_student(student, course)
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
            return Response({"message": "Matrícula cancelada com Sucesso!"}, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": "Erro na solicitação", "detals": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Erro inesperado", "details": str(e)}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    '''
    Método Listagem dos Alunos ativos matrículados em Determinado Curso
    Disclaimer: Normalmente eu deixaria essa lógica em Courses pois creio que faz mais sentido, e não aqui. 
    Mas como nos requisitos essa lógica estava especificado no ponto 4. Matrícula de Aluno, decidi deixar aqui para ficar conforme o escopo.
    '''
    @action(detail=True, methods=['get'], url_path='students-by-course', serializer_class=StudentRegistrationSerializer)
    def students_by_course(self, request, pk=None):
        try:
            registrations = StudentRegistration.objects.filter(courses__id=pk, is_active=True)
            serializer = StudentRegistrationSerializer(registrations, many=True)
        except StudentRegistration.DoesNotExist:
            return Response({"error": "Nenhuma matrícula encontrada para este curso."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)



