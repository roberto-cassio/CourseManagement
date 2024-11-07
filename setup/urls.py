from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from coursemanagement.views.teacher_views import TeacherViewSet



router = routers.DefaultRouter()
router.register('teachers', TeacherViewSet, basename="Teachers")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
