from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification, PushSubscription
from .serializers import NotificationSerializer, PushSubscriptionSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class NotificationMarkReadView(APIView):
    def post(self, request, pk, *args, **kwargs):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response({"status": "read"})

class PushSubscriptionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PushSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            PushSubscription.objects.update_or_create(
                user=request.user,
                endpoint=serializer.validated_data['endpoint'],
                defaults={
                    'p256dh': serializer.validated_data['p256dh'],
                    'auth': serializer.validated_data['auth']
                }
            )
            return Response({"status": "subscribed"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        endpoint = request.data.get('endpoint')
        if not endpoint:
            return Response({"error": "endpoint is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        deleted, _ = PushSubscription.objects.filter(user=request.user, endpoint=endpoint).delete()
        if deleted:
            return Response({"status": "unsubscribed"}, status=status.HTTP_200_OK)
        return Response({"error": "subscription not found"}, status=status.HTTP_404_NOT_FOUND)
