from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from coursemanagement.views.teacher_views import TeacherViewSet
from coursemanagement.views.student_views import StudentViewSet



router = routers.DefaultRouter()
router.register('teachers', TeacherViewSet, basename="Teachers")
router.register('students', StudentViewSet, basename="Students" )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
