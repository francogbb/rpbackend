from rest_framework.routers import DefaultRouter
from .views.profileView import ProfileViewSet
from .views.customGroupView import CustomGroupViewSet
from .views.groupUserView import GroupUserViewSet
from .views.customUserView import CustomUserView, CustomUserProfView

router = DefaultRouter()

router.register(r'register', CustomUserView, basename='register')
router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'customGroup', CustomGroupViewSet, basename='customGroup')
router.register(r'groupUser', GroupUserViewSet, basename='groupUser')
router.register(r'customUserPro', CustomUserProfView, basename='profileCustom')

 
urlpatterns = router.urls