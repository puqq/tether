from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import RegisterUser, UserListView, RelationshipViewSet

def home(request):
    # You could remove this or keep it simple. If removed, remove references to it in urlpatterns.
    from django.http import HttpResponse
    return HttpResponse("Welcome to the Tether app (React-Only).")

router = routers.DefaultRouter()
router.register(r'relationships', RelationshipViewSet, basename='relationship')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterUser.as_view(), name='register-user'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('accounts/', include('allauth.urls')),  # If using Allauth's default forms
    path('', home, name='home'),
]

urlpatterns += router.urls
