from django.shortcuts import render, HttpResponse, redirect,get_object_or_404
from .models import Blog, Category, Comment,PostView,Like
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from .forms import CommentForm
from django.contrib.auth import get_user 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class ToggleLikeView(View):
    def post(self, request, slug):
        if not request.user.is_authenticated:
            return redirect('login')  # Giriş yapmamışsa hata verme

        blog = get_object_or_404(Blog, slug=slug)

        # Sadece giriş yapmış ve geçerli kullanıcılar için işlem yap
        if not request.user.id:
            return redirect('blog_detail', slug=slug)

        like_qs = Like.objects.filter(blog=blog, user=request.user)

        if like_qs.exists():
            like_qs.delete()
        else:
            try:
                
                Like.objects.create(blog=blog, user=request.user)
            except Exception as e:
                print(f"Like oluşturulurken hata: {e}")
        
        return redirect('blog_detail', slug=slug)

class BlogList(View):
    def get(self,request):
        blogs = Blog.objects.all()
        return render(request, 'blog.html', {'blogs':blogs})   
    
    
class BlogDetail(View):
    def get(self, request, slug):
        blog = get_object_or_404(Blog, slug=slug)

        # Görüntülenme kaydını oluştur
        PostView.objects.create(blog=blog)

        # Toplam görüntülenme sayısı
        total_views = PostView.objects.filter(blog=blog).count()
        
        # Sayılar
        comment_count = Comment.objects.filter(blog=blog).count()
        like_count = Like.objects.filter(blog=blog).count()
        categories = Category.objects.all()
        
        # Yorumlar ve form
        comments = Comment.objects.filter(blog=blog)
        comment_form = CommentForm()

        # Kullanıcı beğenmiş mi?
        is_liked = False
        if request.user.is_authenticated:
            is_liked = Like.objects.filter(blog=blog, user=request.user).exists()


        return render(request, 'blog_detail.html', {
            'image': blog.image.url,
            'blog': blog,
            'categories': categories,
            'total_views': total_views,
            'comment_count': comment_count,
            'like_count': like_count,
            'current_slug': slug,
            'comments': comments,
            'comment_form': comment_form,
            'is_liked': is_liked  # <-- burası önemli!
        })


class BlogList(View):
    def get(self, request):
        blogs = Blog.objects.all()  # Tüm blogları al
        categories = Category.objects.all()  # Tüm kategorileri al

        return render(request, 'blog.html', {
            'blogs': blogs,  # Blogları şablona gönder
            'categories': categories,  # Kategorileri şablona gönder
            'current_slug': None  # Aktif kategori yok
        })
    
class CategoryBlog(View):
    def get(self, request, slug):
        categories = Category.objects.all()  # Tüm kategorileri al
        category = get_object_or_404(Category, slug=slug)  # Seçilen kategoriyi al
        blogs = category.blogs.all()  # Seçilen kategoriye ait blogları al

        return render(request, 'blog.html', {
            'blogs': blogs,  # Blogları şablona gönder
            'categories': categories,  # Kategorileri şablona gönder
            'current_slug': slug  # Aktif kategori slug'ını gönder
        })
    
class Login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print('login başarılı')
            return redirect('blog')
        return render(request, 'login.html')


class Logout(View):
    def get(self,request):
        messages.success(request, 'Çıkış işlemi başarılı')
        return redirect('login')
    

class Register(View):
    def get(self,request):
        return render(request,'register.html')
    
    def post(self,request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1=request.POST.get('password')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            print(f'{user.username} kayıt edildi')
            return redirect('login')
        else:
            messages.error(request,'Şifreler aynı değil')
            return redirect('register')




class ToggleLikeView(View):
    def post(self, request, slug):
        if not request.user.is_authenticated:
            return redirect('login')  # Giriş yapmamışsa

        blog = get_object_or_404(Blog, slug=slug)
        like_qs = Like.objects.filter(blog=blog, user=request.user)

        if like_qs.exists():
            like_qs.delete()  # beğeniyi kaldır
        else:
            Like.objects.create(blog=blog, user=request.user)  # beğeni oluştur

        return redirect('blog_detail', slug=slug)


