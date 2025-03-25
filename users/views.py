from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializers import RegisterSerializer, LoginSerializer, UserResponseSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User created successfully",
                "user": UserResponseSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return Response({
                    "message": "Login successful",
                    "user": UserResponseSerializer(user).data
                })
            return Response({
                "message": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({
            "message": "Successfully logged out"
        }, status=status.HTTP_200_OK)

