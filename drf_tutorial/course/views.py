# import json
# from django.http import JsonResponse, HttpResponse
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.views import View
#
# # Create your views here.
#
# course_dict = {
#     'name': '课程名称',
#     'introduction': '课程介绍',
#     'price': 0.11
# }
#
# # Django FBV 编写API接口
# @csrf_exempt
# def course_list(request):
#     if request.method == 'GET':
#         # return HttpResponse(json.dumps(course_dict, ensure_ascii=False), content_type='application/json')
#         return JsonResponse(course_dict)
#
#     if request.method == 'POST':
#         course = json.loads(request.body.decode('utf-8'))
#         # return HttpResponse(json.dumps(course, ensure_ascii=False), content_type='application/json')
#         return JsonResponse(course, safe=False)
#
#
# # Django CBV 编写API接口
# @method_decorator(csrf_exempt, name='dispatch')
# class CourseList(View):
#
#     def get(self, request):
#         return JsonResponse(course_dict)
#
#     # @csrf_exempt
#     def post(self, request):
#         course = json.loads(request.body.decode('utf-8'))
#         return JsonResponse(course, safe=False)







# --------------------------Rest Framework------------------------------

from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer

# 方法一
from rest_framework.decorators import api_view
# 方法二
from rest_framework.views import APIView
# 方法三
from rest_framework import generics
# 方法四
from rest_framework import viewsets

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication

from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerReadOnly

""" 函数式编程 Function Based View"""
@api_view(['GET', 'POST'])
@authentication_classes((BasicAuthentication, TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def course_list(request):
    """
    获取所有课程或新增一个课程
    """
    if request.method == 'GET':
        s = CourseSerializer(instance=Course.objects.all(), many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        s = CourseSerializer(data=request.data)
        # 部分更新用partial=True属性
        # s = CourseSerializer(data=request.data, partial=True)
        if s.is_valid():
            s.save(teacher=request.user)
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes((BasicAuthentication, TokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated,))
def course_detail(request, pk):
    """
    获取、更新、删除一个课程
    """

    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)
    else:
        if request.method == 'GET':
            s = CourseSerializer(instance=course)
            return Response(data=s.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            s = CourseSerializer(instance=course, data=request.data)
            if s.is_valid():
                s.save()
                return Response(data=s.data, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            course.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


""" 类视图编程 Function Based View"""
class CourseList(APIView):

    authentication_classes = (BasicAuthentication, TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Course.objects.all()
        s = CourseSerializer(instance=queryset, many=True) # instance = xx 是数据库查询集
        print(self.request.user, self.request.auth)
        print(type(self.request.user), type(self.request.auth))
        return Response(data=s.data, status=status.HTTP_200_OK)

    def post(self, request):
        s = CourseSerializer(data=request.data) # data = xx 是客户端发送数据，return前要先调用.is_valid()方法
        if s.is_valid():
            s.save(teacher=self.request.user)
            print(type(request.data), type(s.data))
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetail(APIView):

    authentication_classes = (BasicAuthentication, TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get_object( pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)
        s = CourseSerializer(instance=course)
        return Response(data=s.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(data={"msg": "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)
        s = CourseSerializer(instance=course, data=request.data)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_200_OK)
        return Response(data=s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response(data={"msg", "没有此课程信息"}, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------------------------通用类视图------------------------------

class GCourseList(generics.ListCreateAPIView):

    authentication_classes = (BasicAuthentication, TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)

class GCourseDetail(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = (BasicAuthentication, TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerReadOnly)

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# --------------------------视图集viewset------------------------------

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = (BasicAuthentication, TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


# --------------------------Token----------------------------------
from django.db.models.signals import post_save
# from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender, instance=None, created=False, **kwargs):
    """
    创建用户时自动生成Token
    """
    if created:
        Token.objects.create(user=instance)