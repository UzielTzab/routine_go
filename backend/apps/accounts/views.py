from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.settings import api_settings

def _set_cookie(response, key, value, lifetime_property):
    # lifetime_property es ej: 'ACCESS_TOKEN_LIFETIME'
    max_age = getattr(api_settings, lifetime_property).total_seconds()
    response.set_cookie(
        key=key,
        value=value,
        max_age=int(max_age),
        httponly=True,
        samesite='None',
        secure=True
    )

class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
            
            if access_token:
                _set_cookie(response, 'access_token', access_token, 'ACCESS_TOKEN_LIFETIME')
            if refresh_token:
                _set_cookie(response, 'refresh_token', refresh_token, 'REFRESH_TOKEN_LIFETIME')
                
            # Opcionalmente, eliminar tokens del payload JSON por seguridad estricta
            # response.data.pop('access', None)
            # response.data.pop('refresh', None)
            # Pero mantenemos 'access' por si el cliente legacy lo requiere, aunque se recomendó remover. 
            # El requerimiento dice: "en lugar de (o además de)". Lo mantenemos para evitar romper tests legacy inmediatos, 
            # pero devolvemos en cookie.
        return response

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        # Si el cliente envía en la cookie, lo inyectamos al request.data
        refresh_cookie = request.COOKIES.get('refresh_token')
        if refresh_cookie and 'refresh' not in request.data:
            # Clonamos request.data para inyectar si es inmutable
            if hasattr(request.data, '_mutable'):
                request.data._mutable = True
            request.data['refresh'] = refresh_cookie

        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data.get('access')
            if access_token:
                _set_cookie(response, 'access_token', access_token, 'ACCESS_TOKEN_LIFETIME')
            
            refresh_token = response.data.get('refresh')
            if refresh_token:
                _set_cookie(response, 'refresh_token', refresh_token, 'REFRESH_TOKEN_LIFETIME')
        return response

from rest_framework.permissions import AllowAny

class LogoutView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token', samesite='None')
        response.delete_cookie('refresh_token', samesite='None')
        return response

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            response = Response({
                "user": serializer.data,
                "access": access_token,
                "refresh": refresh_token
            }, status=status.HTTP_201_CREATED)
            
            _set_cookie(response, 'access_token', access_token, 'ACCESS_TOKEN_LIFETIME')
            _set_cookie(response, 'refresh_token', refresh_token, 'REFRESH_TOKEN_LIFETIME')
            
            return response
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
