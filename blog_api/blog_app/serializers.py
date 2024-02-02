from rest_framework import serializers
from .models import Category, Post

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "description", "slug")
        read_only_fields = ("slug",)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("title", "content", "user", "category", "image", "is_published", "publish_date")
        

class ReadPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ("title", "content", "user", "category", "image", "is_published", "publish_date", "views")
        read_only_fields = ('views',)





