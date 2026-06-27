from rest_framework import serializers
from blogapp.models import Comment,Blog,Category

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
       
class UserBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['status']
    
