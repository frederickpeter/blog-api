from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action
from django.db.models import F
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CategorySerializer, ReadPostSerializer, PostSerializer
from .models import Category, Post
from .filters import PostFilter
from blog_api.utils.pagination import LargeResultsSetPagination

# Create your views here.
class CategoryViewset(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.order_by('name')

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        return [AllowAny()]


class PostViewset(ModelViewSet):
    pagination_class = LargeResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = PostFilter
    search_fields = ['title']
    ordering_fields = ['title', 'publish_date']

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user).select_related('user', 'category').order_by('-publish_date') if user else Post.objects.none()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadPostSerializer
        return PostSerializer
    
    def get_permissions(self):
        if self.action in ["all_posts", "retrieve_post"]:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
        

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        serializer = ReadPostSerializer(data)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = PostSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        data = self.perform_update(serializer)
        serializer = ReadPostSerializer(data)
        return Response(serializer.data)
    
    # http://127.0.0.1/posts/all/
    @action(detail=False, methods=["GET"], url_path="all", serializer_class=ReadPostSerializer)
    def all_posts(self, request):
        queryset = self.filter_queryset(Post.objects.filter(is_published=True).select_related('user', 'category').order_by('-publish_date'))
        serializer = ReadPostSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # http://127.0.0.1/posts/1/retrieve
    @action(detail=True, methods=["GET"], url_path="retrieve", serializer_class=ReadPostSerializer)
    def retrieve_post(self, request, pk=None):
        try:
            instance = Post.objects.get(pk=pk, is_published=True)
            instance.views = F('views') + 1
            instance.save()
            serializer = ReadPostSerializer(instance)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({'status':'no post found'}, status=status.HTTP_404_NOT_FOUND)


