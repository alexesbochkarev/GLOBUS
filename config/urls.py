from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from users.views import UserCreateViewSet
from apps.chats.views import RoomViewSet

from config.yasg import urlpatterns as doc_urls

router = DefaultRouter()

router.register(r'user', UserCreateViewSet, basename='user')
router.register(r'room', RoomViewSet, basename='room')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', include(router.urls)),
]

urlpatterns += doc_urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
