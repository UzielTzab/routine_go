from django.urls import path
from .views import NotificationListView, NotificationMarkReadView, PushSubscriptionView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<uuid:pk>/read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('subscriptions/', PushSubscriptionView.as_view(), name='push-subscription'),
]
