from django.urls import path
from .views.userViews import (CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView, LogoutView)


#endpoints djoser: https://djoser.readthedocs.io/en/latest/base_endpoints.html
urlpatterns = [
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
]