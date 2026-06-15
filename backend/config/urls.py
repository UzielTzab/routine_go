from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.common.urls')),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/routines/', include('apps.routines.urls')),
    path('api/schedule/', include('apps.schedule.urls')),
    path('api/executions/', include('apps.executions.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]
