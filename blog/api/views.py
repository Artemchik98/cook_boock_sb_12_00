from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import PostSerializer, PostPointSerializer, CommentSerializer
from ..models import Post, PostPoint, Comment


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostPointViewSet(viewsets.ModelViewSet):
    queryset = PostPoint.objects.all()
    serializer_class = PostPointSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer




@api_view(["GET"])
def post_list(request):
    objects = Post.objects.all()
    serializer_class = PostSerializer(objects, many=True)
    return Response(serializer_class.data)


@api_view(['GET'])
def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    post_serializer = PostSerializer(post)
    post_points = PostPoint.objects.filter(post=post)
    post_points_serializer = PostPointSerializer(
        post_points, many=True)
    return Response({'post': post_serializer.data,
                     'post_points': post_points_serializer.data})


@api_view(['POST'])
def post_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['PUT'])
def post_update(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(data=request.data,
                                instance=post)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def post_delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return JsonResponse(
        {'deleted': status.HTTP_204_NO_CONTENT})
@api_view(["GET"])
def post_list(request):
    objects = Post.objects.all()
    serializer_class = PostSerializer(objects, many=True)
    return Response(serializer_class.data)

@api_view(["GET"])
def post_detail(request,pk):
    post=Post.objects.get(id=pk)
    post_serializer = PostSerializer(post)
    return Response({'post':post_serializer.data})

@api_view(['POST'])
def post_create(request):
    serializer=PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def post_point_create(request):
    serializer=PostPointSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
def post_update(request,pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(data=request.data,
                                instance=post)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def post_delete(request,pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return JsonResponse({'deleted, status':status.HTTP_204_NO_CONTENT})
