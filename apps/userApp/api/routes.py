from rest_framework.routers import DefaultRouter
from .views.userView import UserViewSet
from .views.profileView import ProfileViewSet
from .views.customGroupView import CustomGroupViewSet
from .views.groupUserView import GroupUserViewSet

router = DefaultRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'customGroup', CustomGroupViewSet, basename='customGroup')
router.register(r'groupUser', GroupUserViewSet, basename='groupUser')

urlpatterns = router.urls