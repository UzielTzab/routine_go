from django.contrib import admin
from django.urls import path, include
from apps.accounts.views import CookieTokenObtainPairView, CookieTokenRefreshView, LogoutView, RegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.common.urls')),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/routines/', include('apps.routines.urls')),
    path('api/schedule/', include('apps.schedule.urls')),
    path('api/executions/', include('apps.executions.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
]
