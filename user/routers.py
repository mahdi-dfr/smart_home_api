from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *

router = DefaultRouter()
router.register('management', UserManagement, basename='user_management'),

urlpatterns = [
                  path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('me/', MeView.as_view(), name='me'),
              ] + router.urls
