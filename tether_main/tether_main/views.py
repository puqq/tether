# tether_main/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from allauth.account.models import EmailAddress
from allauth.account.forms import SignupForm

from .models import Relationship
from .serializers import UserSerializer, RelationshipSerializer

class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes     = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get("login") or request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"detail": "Login successful!"})
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        data = {
            "username":  request.data.get("username"),
            "email":     request.data.get("email"),
            "password1": request.data.get("password1"),
            "password2": request.data.get("password2"),
        }
        form = SignupForm(data=data, request=request)
        if form.is_valid():
            user = form.save(request)
            EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return Response({"detail": "User created and logged in."}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Form errors", "errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        qs = User.objects.all()
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)

class CurrentUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class RelationshipViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class   = RelationshipSerializer
    def get_queryset(self):
        return Relationship.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TestEmailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            rel = Relationship.objects.get(pk=pk, user=request.user)
        except Relationship.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        subject = f"Tether Test Email for {rel.contact_name}"
        message = (
            f"Hi {request.user.username},\n\n"
            f"This is a test reminder for your contact {rel.contact_name}.\n"
            f"Relationship type: {rel.relationship_type}\n"
            f"Frequency: {rel.reminder_frequency}\n\n"
            "— Sent via Tether test endpoint."
        )
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=False)
        except Exception as e:
            return Response({"detail": f"Failed to send: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "Test email sent"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({"detail": "Logged out"}, status=200)