from django.contrib import admin
from django.urls import path, include
# - IMPORT para el JWT Token -----------------------------------------------
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
# - IMPORTS para archivos estáticos ------------------------------------------
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/', include('apps.userApp.api.urls')),
    path('api/', include('apps.userApp.api.routes')),
    path('api/', include('apps.academicApp.api.routes')),
    path('api/', include('apps.documentApp.api.routes')),
<<<<<<< HEAD

=======
>>>>>>> 59e6363e3e350b541981b7bd909634c8b6c78d6f
]




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  