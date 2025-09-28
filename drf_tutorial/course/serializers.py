from rest_framework import serializers
from django.contrib.auth.models import User
from course.models import Course
from django import forms

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'introduction', 'teacher', 'price')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    teacher = serializers.ReadOnlyField(source='teacher.username')
    class Meta:
        model = Course
        # exclude = ('id', )
        # fields = ('id', 'name', 'introduction', 'teacher', 'price', 'created_at', 'updated_at')
        fields = '__all__'
        depth = 2

# class CourseSerializer(serializers.HyperlinkedModelSerializer):
#     teacher = serializers.ReadOnlyField(source='teacher.username')
#     class Meta:
#         model = Course
#         # exclude = ('id', )
#         fields = ('id', 'url', 'name', 'introduction', 'teacher', 'price', 'created_at', 'updated_at')
