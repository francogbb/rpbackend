from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

class CustomTokenObtainPairView(TokenObtainPairView):
    
    def post(self, request, *args, **kwargs):
        # Obtenemos la respuesta
        response = super().post(request, *args, **kwargs)

        # Se obtienen los tokens
        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')
        
            # Se setean las cookies del token de access y refresh
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response

class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        
        # Se obtiene el token refresh desde las cookies
        refresh_token = request.COOKIES.get('refresh')

        # El valor 'refresh' de la data tomará el valor del refresh_token
        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)
        
        # Se obtiene el token de acceso de la respuesta
        if response.status_code == 200:
            access_token = response.data.get('access')
        
        # Se setea en las cookies el token de acceso
            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
        
        return response
    
class CustomTokenVerifyView(TokenVerifyView):

    def post(self, request, *args, **kwargs):

        # Se obtiene el token de acceso desde las cookies
        access_token = request.COOKIES.get('access')

        # El valor 'token' de la data tomará el valor del access_token
        if access_token:
            request.data['token'] = access_token

        # Retorna la solicitud
        return super().post(request, *args, **kwargs)
    
class LogoutView(APIView):
    
    def post(self, request, *args, **kwargs):
        
        response = Response(status = status.HTTP_204_NO_CONTENT)

        # Se eliminan los tokens access y refresh de las cookies
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
