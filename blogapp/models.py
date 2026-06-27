from django.db import models
from slugify import slugify
from django import forms
from django.conf import settings

# Create your models here.




class Status(models.TextChoices):
    d='d','draft'
    p='p','published'
class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name="Başlık")
    content = models.TextField(verbose_name="İçerik")
    publish_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="blog")
    status = models.CharField(max_length=1,choices=Status.choices,default=Status.d)
    slug = models.SlugField(unique=True, null=True, blank=True)
    user = models.ForeignKey(
        'blogapp.User',
        on_delete=models.CASCADE, 
        related_name='blogs',
        null=True,
        verbose_name='kullanici'

    )
    category = models.ForeignKey(
        'blogapp.Category', 
        on_delete=models.CASCADE, 
        related_name='blogs',
        null=True,
        verbose_name='kategori'
    )

    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    
    def total_comments(self):
       return self.comments.count()
    
    def total_likes(self):
        return self.likes.count()
    



class Category(models.Model):
    name = models.CharField(max_length=100 , verbose_name='kategori')
    slug = models.SlugField(unique=True, blank=True)
    blog= models.ForeignKey(
        'blogapp.Blog',
        on_delete=models.CASCADE, 
        related_name='categories',
        null=True,
        blank=True
    ) 

    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    

    

class User(models.Model):
    name = models.CharField(max_length=100, verbose_name='kullanici')

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    content=models.TextField(verbose_name='icerik')
    time_stamp=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        null=False,
        related_name='comments',
        

    )
    blog= models.ForeignKey(
        'blogapp.Blog',
        on_delete=models.CASCADE, 
        related_name='comments',
        

    )
    

    def __str__(self):
        return f'{self.user.name} - {self.blog.title}'



class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        null=True,
        default=1
        
        
    )
    blog= models.ForeignKey(
        'blogapp.Blog',
        on_delete=models.CASCADE, 
        related_name='likes',
        null=True,
        default=1
        

    )
    class Meta:
        unique_together = ('user', 'blog')  # her kullanıcı bir blogu 1 kere beğenebilir


    def __str__(self):
        user = self.user if self.user else "Anonim"
        blog = self.blog if self.blog else "Bilinmeyen Blog"
        return f"{user} - {blog} <3"
    

class PostView(models.Model):
    post_views = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(
        'blogapp.User',
        on_delete=models.CASCADE,
        related_name='views',
        null=True,
    
    )
    blog = models.ForeignKey(
        'blogapp.Blog', 
        on_delete=models.CASCADE, 
        related_name='views',
        null=True
        )
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.post_views)