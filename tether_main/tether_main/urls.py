# tether_main/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import logout_view
from rest_framework.routers import DefaultRouter
from .views import (
    LoginAPIView,
    RegisterUser,
    UserListView,
    TestEmailAPIView,
    CurrentUserAPIView,
    logout_view,
    RelationshipViewSet,
)

router = DefaultRouter()
router.register(r'relationships', RelationshipViewSet, basename='relationship')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/login/', LoginAPIView.as_view()),
    path('api/logout/', logout_view, name='api-logout'),
    path('api/register/', RegisterUser.as_view()),

    path('api/users/',       UserListView.as_view()),
    path('api/users/me/',    CurrentUserAPIView.as_view(), name='current-user'),
    
    path('api/', include(router.urls)),
    path('api/send-test-email/<int:pk>/', TestEmailAPIView.as_view(), name='send-test-email'),
]
