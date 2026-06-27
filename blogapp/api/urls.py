from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'blogs', BlogModelViewSet, basename='blog')
router.register(r'categories', CategoryModelViewSet, basename='category')
router.register(r'comments', CommentModelViewSet, basename='comment')



urlpatterns = [
     path('router/', include(router.urls)),
]
