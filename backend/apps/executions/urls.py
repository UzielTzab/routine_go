from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoutineExecutionViewSet

router = DefaultRouter()
router.register(r'', RoutineExecutionViewSet, basename='execution')

urlpatterns = [
    path('', include(router.urls)),
]
