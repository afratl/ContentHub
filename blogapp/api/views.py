from rest_framework.views import APIView
from blogapp.models import Blog, Comment, Category
from rest_framework.response import Response
from rest_framework import status
from .serializer import BlogSerializer, CommentSerializer, CategorySerializer,UserBlogSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .permissions import IsOwnerOrStaffOrReadOnly
from django.db.models import Q


class BlogModelViewSet(ModelViewSet):
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Blog.objects.all()
        if user.is_authenticated:
            return Blog.objects.filter(
                Q(status='p') | Q(status='d', author=user)
            )
        return Blog.objects.filter(status='p')

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff:
            return BlogSerializer
        return UserBlogSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    

class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    

class CategoryModelViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class UserBlogModelView(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = UserBlogSerializer



