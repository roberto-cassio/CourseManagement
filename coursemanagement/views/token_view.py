from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg.utils import swagger_auto_schema

class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(tags=["Autenticação"], operation_summary="Obtenha o token JWT")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
