from apps.core.routers import DefaultRouter
from apps.users.views import UserViewSet, SignUpViewSet, FileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='users')
router.register(r'sign-up', SignUpViewSet, base_name='sign_up')
router.register(r'file', FileViewSet, base_name='file')
