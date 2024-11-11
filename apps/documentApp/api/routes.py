from rest_framework.routers import DefaultRouter
from .views.applicationFormView import ApplicationFormViewSet
from .views.documentView import DocumentViewSet, DocumentPublicViewSet
from .views.publishFormView import PublishFormViewSet
from .views.recordView import RecordViewSet
from .views.statisticsView import StatisticsViewSet
from .views.typeDocumentView import TypeDocumentViewSet

router = DefaultRouter()

router.register(r'applicationForm', ApplicationFormViewSet, basename='applicationForm')
router.register(r'document', DocumentViewSet, basename='document')
router.register(r'viewDocument', DocumentPublicViewSet, basename='documentPublic')
router.register(r'publishForm', PublishFormViewSet, basename='publishForm')
router.register(r'record', RecordViewSet, basename='record')
router.register(r'statistics', StatisticsViewSet, basename='statistics')
router.register(r'typeDocument', TypeDocumentViewSet, basename='typeDocument')

urlpatterns = router.urls

from django.urls import path

urlpatterns += [
    path('document/<int:pk>/desencriptar/', DocumentViewSet.as_view({'get': 'desencriptar_documento'})),
]

