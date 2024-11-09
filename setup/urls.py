from django.contrib import admin
from django.urls import path, include

from rest_framework import routers, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from coursemanagement.views.teachers_views import TeacherViewSet
from coursemanagement.views.students_views import StudentViewSet
from coursemanagement.views.courses_views import CoursesViewSet
from coursemanagement.views.classes_views import ClassesViewSet
from coursemanagement.views.students_registration_views import StudentRegistrationViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Online Courses API",
        default_version='v1',
        description="Documentação da API para o projeto de criação de API para Cursos Online",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[],
)


router = routers.DefaultRouter()
router.register('teachers', TeacherViewSet, basename="Teachers")
router.register('students', StudentViewSet, basename="Students" )
router.register('courses', CoursesViewSet, basename="Courses")
router.register('classes', ClassesViewSet, basename="Classes")
router.register("registration", StudentRegistrationViewSet, basename="Student_Registration" )

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]

#Swagger
urlpatterns += [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]