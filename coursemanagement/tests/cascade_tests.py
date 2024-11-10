from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIRequestFactory

from coursemanagement.models.courses import Courses
from coursemanagement.models.classes import Classes
from coursemanagement.models.students import Student
from coursemanagement.models.students_registration import StudentRegistration
from coursemanagement.models.teachers import Teacher
from coursemanagement.services.soft_delete_service import delete_teacher_and_associated_courses, is_deleted, delete_course_and_associated_registrations
from coursemanagement.views.base_model_view_set import SoftDeleteModelViewSet

class TeacherCourseDeletionTestCase(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            name="Professor Teste",
            email="professor@teste.com"
        )
        
        self.course = Courses.objects.create(
            title="Curso Teste",
            teacher=self.teacher,
            workload= 40
        )

        self.class1 = Classes.objects.create(
            name="Aula Teste 1",
            courses=self.course,
            duration=timedelta(days=1, seconds=3600),
            date = timezone.now()
        )
        self.class2 = Classes.objects.create(
            name="Aula Teste 2",
            courses=self.course,
            duration=timedelta(days=1, seconds=3600),
            date = timezone.now()
        )

        self.student = Student.objects.create(
            name="Aluno Teste",
            email="aluno@teste.com"
        )

        self.registration = StudentRegistration.objects.create(
            student=self.student,
            courses=self.course,
            enrollment_date = timezone.now(),
            is_active=True
        )
        self.user = User.objects.create_user(username='testuser', password='password')

        
        # Gerar o JWT Token 
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        
        # Inicializando o cliente de API com o token JWT
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_teacher_delete_cascade(self):
        # Verifica se o Teacher e os objetos associados existem
        self.assertEqual(Teacher.objects.count(), 1)
        self.assertEqual(Courses.objects.count(), 1)
        self.assertEqual(Classes.objects.count(), 2)
        self.assertEqual(StudentRegistration.objects.count(), 1)

        # Deletando o Professor
        delete_teacher_and_associated_courses(self.teacher)

        '''Verifica se, após a deleção do professor, os cursos, aulas, e matrículas foram devidamente deletadas/canceladas'''
        self.teacher.refresh_from_db()
        self.assertIsNotNone(self.teacher.deleted_at)

        self.course.refresh_from_db()
        self.assertIsNotNone(self.course.deleted_at)

        self.class1.refresh_from_db()
        self.class2.refresh_from_db()
        self.assertIsNotNone(self.class1.deleted_at)
        self.assertIsNotNone(self.class2.deleted_at)

        # Verifica se as StudentRegistrations foram desativadas (is_active=False)
        self.registration.refresh_from_db()
        self.assertFalse(self.registration.is_active)
        self.assertIsNotNone(self.registration.cancellation_date)

    
    def test_teacher_delete_with_no_courses(self):
        another_teacher = Teacher.objects.create(
            name="Outro Professor",
            email="outro@teste.com"
        )
        another_course = Courses.objects.create(
            title="Curso Outro",
            teacher=another_teacher,
            workload=20
        )
        another_registration = StudentRegistration.objects.create(
            student=self.student,
            courses=another_course,
            enrollment_date = timezone.now(),
            is_active=True
        )
        self.assertEqual(Courses.objects.count(), 2)
        
        delete_teacher_and_associated_courses(self.teacher)


        another_course.refresh_from_db()
        self.assertIsNone(another_course.deleted_at)
        
        another_registration.refresh_from_db()
        self.assertTrue(another_registration.is_active)
    
    
    def test_course_delete(self):
        self.assertEqual(Courses.objects.count(), 1)
        self.assertEqual(Classes.objects.count(), 2)
        self.assertEqual(StudentRegistration.objects.count(), 1)

        delete_course_and_associated_registrations(self.course)

        self.course.refresh_from_db()
        self.assertIsNotNone(self.course.deleted_at)

        self.class1.refresh_from_db()
        self.class2.refresh_from_db()
        self.assertIsNotNone(self.class1.deleted_at)
        self.assertIsNotNone(self.class2.deleted_at)

        self.registration.refresh_from_db()
        self.assertFalse(self.registration.is_active)
        self.assertIsNotNone(self.registration.cancellation_date)

        self.student.refresh_from_db()
        self.assertIsNone(self.student.deleted_at)

        self.teacher.refresh_from_db()
        self.assertIsNone(self.teacher.deleted_at)