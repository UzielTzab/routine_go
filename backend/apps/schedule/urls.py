from django.urls import path
from .views import TodayScheduleView

urlpatterns = [
    path('today/', TodayScheduleView.as_view(), name='schedule-today'),
]
