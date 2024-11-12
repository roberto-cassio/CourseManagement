from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    http_method_names= ['get', 'post']

    '''O Get só vai buscar alunos com a Matrícula efetivamente active ou inactive de acordo com o parâmetro de consulta "status". O Default é active.'''
    def get_queryset(self):
        status_filter = self.request.query_params.get('status', 'active')
        if status_filter == 'active':
            return StudentRegistration.objects.filter(is_active=True)
        if status_filter == 'inactive':
            return StudentRegistration.objects.filter(is_active=False)
        else:
            return StudentRegistration.objects.all()

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
        '''Método para cancelar uma matrícula de um estudante em um curso específico. A matrícula será marcada como inativa e a data de cancelamento será registrada.'''
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
    @swagger_auto_schema(
            manual_parameters=[
            openapi.Parameter(
                'id', openapi.IN_PATH, description='Identificador único do curso para buscar estudantes matriculados',
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    @action(detail=True, methods=['get'], url_path='students', serializer_class=StudentRegistrationSerializer)
    def students_by_course(self, request, pk=None):
        '''Retorna a lista de estudantes matriculados em um curso específico.'''
        try:
            registrations = StudentRegistration.objects.filter(courses__id=pk, is_active=True)
            serializer = StudentRegistrationSerializer(registrations, many=True)
        except StudentRegistration.DoesNotExist:
            return Response({"error": "Nenhuma matrícula encontrada para este curso."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)
    

