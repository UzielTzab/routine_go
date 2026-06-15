from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, RoutineTemplateViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'templates', RoutineTemplateViewSet, basename='routinetemplate')

urlpatterns = router.urls
