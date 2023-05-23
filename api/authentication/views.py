from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from api.authentication.serializers import UserSerializer, ChangeLoginSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
                email=serializer.validated_data.get('email')
            )
            return Response({'message': 'User created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeLoginView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangeLoginSerializer(data=request.data)
        if serializer.is_valid():
            new_username = serializer.validated_data['new_username']
            current_username = request.user.username

            if current_username == new_username:
                return Response({'message': 'New username cannot be the same as the current username.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.exclude(username=current_username).get(username=new_username)
                return Response({'message': 'The new username is already taken. Please choose another.'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                user = User.objects.get(username=current_username)
                user.username = new_username
                user.save()
                return Response({'message': 'Username changed successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
