from rest_framework.routers import DefaultRouter
from .views import StudentViewSet
from django.urls import path, include
from .views import StudentCSVImportView


router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
    path('students/import-csv', StudentCSVImportView.as_view(), name='import-students-csv'),
]
