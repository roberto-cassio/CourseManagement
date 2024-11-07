from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from coursemanagement.views.teachers_views import TeacherViewSet
from coursemanagement.views.students_views import StudentViewSet
from coursemanagement.views.courses_views import CoursesViewSet
from coursemanagement.views.classes_views import ClassesViewSet




router = routers.DefaultRouter()
router.register('teachers', TeacherViewSet, basename="Teachers")
router.register('students', StudentViewSet, basename="Students" )
router.register('courses', CoursesViewSet, basename="Courses")
router.register('classes', ClassesViewSet, basename="Classes")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
