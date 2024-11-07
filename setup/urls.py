from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from coursemanagement.views.teacher_views import TeacherViewSet
from coursemanagement.views.student_views import StudentViewSet
from coursemanagement.views.classes_views import ClassViewSet




router = routers.DefaultRouter()
router.register('teachers', TeacherViewSet, basename="Teachers")
router.register('students', StudentViewSet, basename="Students" )
router.register('classes', ClassViewSet, basename="Classes")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
