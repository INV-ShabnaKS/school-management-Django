from rest_framework.routers import DefaultRouter
from .views import StudentViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]
