from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import StudentProfile, TeacherProfile, User
from .serializers import StudentProfileSerializer, TeacherProfileSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    password = data.pop('password')
    user = User.objects.create_user(
      **data,
      password=password,
    )

    # Create blank role profiles
    if data['role'] == 'student':
      StudentProfile.objects.create(user=user)
    elif data['role'] == 'teacher':
      TeacherProfile.objects.create(user=user)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


class TeacherProfile(generics.RetrieveUpdateAPIView):
  serializer_class = TeacherProfileSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    return self.request.user.teacher_profile


class StudentProfile(generics.RetrieveUpdateAPIView):
  serializer_class = StudentProfileSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    return self.request.user.student_profile
  