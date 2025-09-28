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

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Course
from .serializers import CourseSerializer

""" 函数式编程 Function Based View"""
@api_view(['GET', 'POST'])
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