from django.contrib import admin
from django.urls import path, include
# - IMPORT para el JWT Token -----------------------------------------------
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
# - IMPORTS para archivos estáticos ------------------------------------------
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='get_token'),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path('api/', include('apps.userApp.api.routes')),
    path('api/', include('apps.academicApp.api.routes')),
    path('api/', include('apps.documentApp.api.routes')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  