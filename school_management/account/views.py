from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    password = data.pop('password')

    user = User.objects.create(**data)
    user.set_password(password)
    user.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
