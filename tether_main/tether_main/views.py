# tether_main/views.py
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions

from allauth.account.models import EmailAddress
from allauth.account.forms import SignupForm
from allauth.account.views import LoginView, LogoutView

from .models import Relationship
from .serializers import UserSerializer, RelationshipSerializer

class RegisterUser(APIView):
    def post(self, request):
        data = {
            "username": request.data.get("username"),
            "email": request.data.get("email"),
            "password1": request.data.get("password1"),
            "password2": request.data.get("password2")
        }
        allauth_response = self.register_user_with_allauth(data)

        if allauth_response.status_code in [200, 201, 302]:
            new_user = User.objects.filter(username=data["username"]).first()
            if new_user:
                login(request, new_user, backend='allauth.account.auth_backends.AuthenticationBackend')
            return Response({"detail": "User created and auto-logged in!"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(allauth_response.data, status=status.HTTP_400_BAD_REQUEST)

    def register_user_with_allauth(self, data):
        # Now it's a method of RegisterUser
        signup_form = SignupForm(data=data)
        if signup_form.is_valid():
            user = signup_form.save(self.request)
            email = data["email"]
            EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)
            return Response({"detail": "User created successfully!"},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"detail": "Form errors", "errors": signup_form.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class CustomLoginView(LoginView):
    template_name = 'account/login.html'

class CustomLogoutView(LogoutView):
    next_page = '/'

class RelationshipViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RelationshipSerializer
    queryset = Relationship.objects.all()

    def get_queryset(self):
        return Relationship.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
