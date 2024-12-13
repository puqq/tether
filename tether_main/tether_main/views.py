from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate
from allauth.account.views import LoginView, LogoutView
from .models import Relationship  # Assuming you'll create a Relationship model later
from .serializers import UserSerializer  # If you need custom user serialization


# Register User View (using Django Allauth)
class RegisterUser(APIView):
    def post(self, request):
        # Data should be in the correct format to register a new user using Allauth
        data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password1": request.data.get("password1"),
            "password2": request.data.get("password2")
        }
        
        # Send data to Allauth registration logic (this can be handled by forms or serializers)
        response = self.register_user_with_allauth(data)
        if response.status_code == 201:  # Successful creation
            return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(response.data, status=status.HTTP_400_BAD_REQUEST)

    def register_user_with_allauth(self, data):
        """Use Allauth to register a user"""
        from allauth.account.models import EmailAddress
        from django.contrib.auth import get_user_model
        from allauth.account.forms import SignupForm
        
        user_model = get_user_model()
        signup_form = SignupForm(data=data)
        if signup_form.is_valid():
            user = signup_form.save()
            email = data["email"]
            EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
            return Response({"detail": "User created successfully!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Error creating user."}, status=status.HTTP_400_BAD_REQUEST)

# List All Users View (if you need to list users)
class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()  # Or any custom filtering as needed
        serializer = UserSerializer(users, many=True)  # You may have a custom serializer for User
        return Response(serializer.data)

# User Dashboard View
@login_required
def dashboard(request):
    """Display user-related info, such as relationships"""
    relationships = Relationship.objects.filter(user=request.user)  # Assuming Relationship model
    return render(request, 'dashboard.html', {'relationships': relationships})

# Login View (Handled by Allauth, but can be overridden if customizations are needed)
class CustomLoginView(LoginView):
    template_name = 'account/login.html'  # Customize your template here

# Logout View (Handled by Allauth)
class CustomLogoutView(LogoutView):
    next_page = '/'  # Redirect to home page after logout
