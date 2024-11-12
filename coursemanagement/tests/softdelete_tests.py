from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from django.utils import timezone
from django.contrib.auth.models import User

from coursemanagement.models.students import Student



class SoftDeleteStudentTests(APITestCase):
    def setUp(self):
        '''Auth'''
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Obtém o token JWT
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        """Configurações iniciais para os testes"""
        self.student_data = {
            "name": "John Doe",
            "email": "john@example.com"
        }

        self.student = Student.objects.create(**self.student_data)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)


    def test_soft_delete(self):
        """
        Testa o soft delete, verificando se o campo 'deleted_at' é marcado corretamente.
        """
        # Realiza o soft delete
        url = f'/students/{self.student.id}/'
        response = self.client.delete(url)

        # Verifica se a resposta foi 204 (sucesso, item excluído)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Recarrega a instância para verificar o campo 'deleted_at'
        self.student.refresh_from_db()

        # Verifica se o campo 'deleted_at' foi atualizado
        self.assertIsNotNone(self.student.deleted_at)
        self.assertTrue(self.student.deleted_at <= timezone.now())

    def test_get_queryset_exclude_soft_deleted(self):
        """
        Testa se os objetos soft-deleted são excluídos das listagens padrão.
        """
        # Cria outro estudante para garantir que existam múltiplos
        another_student = Student.objects.create(
            name="Jane Smith", 
            email="jane@example.com"
        )

        # Realiza o soft delete no primeiro objeto
        url = f'/students/{self.student.id}/'
        self.client.delete(url)

        # Faz a requisição para listar os objetos
        url = '/students/'
        response = self.client.get(url)

        # Verifica se o objeto soft-deleted não está na resposta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(
            self.student.name,
            [student['name'] for student in response.data]
        )
        # Verifica se o outro objeto não foi excluído
        self.assertIn(
            another_student.name,
            [student['name'] for student in response.data]
        )

    def test_get_object_after_soft_delete(self):
        """
        Testa se a consulta de um objeto específico não retorna o item após o soft delete,
        e se o campo 'deleted_at' foi preenchido no banco de dados.
        """
        # Realiza o soft delete
        url = f'/students/{self.student.id}/'
        self.client.delete(url)

        # Recarrega a instância para garantir que foi excluída
        self.student.refresh_from_db()

        # Verifica que o campo 'deleted_at' foi preenchido (soft delete)
        self.assertIsNotNone(self.student.deleted_at)

        # Tenta acessar o objeto via GET (não deve ser retornado após soft delete)
        url = f'/students/{self.student.id}/'
        response = self.client.get(url)

        # A resposta deve ser 404 Not Found, já que o objeto foi soft-deletado
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verifica no banco de dados se o 'deleted_at' foi realmente preenchido
        # O campo 'deleted_at' não deve ser None, confirmando o soft delete
        student_in_db = Student.objects.get(id=self.student.id)
        self.assertIsNotNone(student_in_db.deleted_at)


    def test_restore_deleted(self):
        """
        Testa se é possível "restaurar" um objeto após o soft delete.
        """
        # Realiza o soft delete
        url = f'/students/{self.student.id}/'
        self.client.delete(url)

        # Recarrega a instância para garantir que foi excluída
        self.student.refresh_from_db()

        # Verifica que o objeto foi excluído com sucesso
        self.assertIsNotNone(self.student.deleted_at)

        # Vamos agora "restaurar" o objeto
        self.student.deleted_at = None  # Restaura o campo deleted_at
        self.student.save()

        # Recarrega novamente
        self.student.refresh_from_db()

        # Verifica se o campo deleted_at foi restaurado para None
        self.assertIsNone(self.student.deleted_at)

    def test_create_student(self):
        """
        Testa a criação de um novo estudante.
        """
        student_data = {
            "name": "Bob Martin",
            "email": "bob@example.com"
        }

        response = self.client.post('/students/', student_data, format='json')

        # Verifica se o status da resposta é 201 (criação com sucesso)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verifica se o estudante foi realmente criado
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(Student.objects.last().name, "Bob Martin")
