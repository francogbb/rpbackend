from rest_framework.routers import DefaultRouter
from .views.sectionView import SectionViewSet
from .views.signatureView import SignatureViewSet
from .views.careerView import CareerViewSet
from .views.areaView import AreaViewSet, AreaModViewSet

router = DefaultRouter()

router.register(r'section', SectionViewSet, basename='section')
router.register(r'signature', SignatureViewSet, basename='signature')
router.register(r'career', CareerViewSet, basename='career')
router.register(r'area', AreaViewSet, basename='area')
router.register(r'areaMod', AreaModViewSet, basename='areaView')

urlpatterns = router.urls