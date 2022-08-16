from rest_framework import serializers

from .models import StudentProfile, TeacherProfile, User

class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

  class Meta:
    model = User
    fields = [
      'id',
      'email',
      'first_name',
      'last_name',
      'age',
      'sex',
      'contact_number',
      'password',
      'role'
    ]


class TeacherProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = TeacherProfile
    fields = [
      'students',
      'subjects'
    ]


class StudentProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = StudentProfile
    fields = [
      'father_name',
      'mother_name',
      'subjects'
    ]