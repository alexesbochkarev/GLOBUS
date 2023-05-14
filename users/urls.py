from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, UserCreateViewSet

router = DefaultRouter()

router.register(r'signup', UserCreateViewSet, basename='user-create')
router.register(r'users', UserViewSet, basename='user-list')


urlpatterns = [
    path('api/v1/', include(router.urls)),
    
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]