"""
URL configuration for tether_main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # Add this import
from . import views  # Import views from the current directory
from .views import RegisterUser, UserListView

# Home view
def home(request):
    return HttpResponse("Welcome to the Tether app!")

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin route
    path('api/register/', RegisterUser.as_view(), name='register-user'),  # User Registration
    path('api/users/', UserListView.as_view(), name='user-list'),  # List All Users
    path('accounts/', include('allauth.urls')),  # AllAuth routes for login, logout, signup, etc. 
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard for logged-in users
    path('', home, name='home'),  # Root URL
]



