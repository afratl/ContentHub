from django.urls import path,include
from . import views
from blogapp.views import ToggleLikeView

urlpatterns = [
    path('', views.BlogList.as_view(), name='blog'),
    path('login', views.Login.as_view(), name='login'),
    path('register', views.Register.as_view(), name='register'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('blog-detay/<slug>',views.BlogDetail.as_view(),name='blog_detail'),
    path('blogs/category/<slug:slug>', views.CategoryBlog.as_view(), name='category_blogs'),
    path('blog/<slug:slug>/like-toggle/', ToggleLikeView.as_view(), name='like_toggle'), 
    path('api/',include('blogapp.api.urls'))
]
