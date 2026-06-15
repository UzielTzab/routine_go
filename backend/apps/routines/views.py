from rest_framework import viewsets, permissions
from .models import Category, RoutineTemplate
from .serializers import CategorySerializer, RoutineTemplateSerializer
from .services.routine_service import create_routine_with_rules, update_routine_with_rules

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class RoutineTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = RoutineTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return RoutineTemplate.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        data = serializer.validated_data
        rules_data = self.request.data.get('schedule_rules', [])
        create_routine_with_rules(self.request.user, data, rules_data)

    def perform_update(self, serializer):
        data = serializer.validated_data
        rules_data = self.request.data.get('schedule_rules', None)
        instance = self.get_object()
        update_routine_with_rules(instance, data, rules_data)
