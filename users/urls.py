from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import UserCreateViewSet, StaffCreateViewSet

router = DefaultRouter()

router.register(r'signup', UserCreateViewSet, basename='user-create')
router.register(r'role', StaffCreateViewSet, basename='role-create')


urlpatterns = [
    path('', include(router.urls))
]