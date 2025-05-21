from rest_framework import serializers
from .models import Blog, MsPost
from accounts.models import UserAuth


class BlogSerializer(serializers.ModelSerializer):
    # author_name = serializers.StringRelatedField(source="author", read_only=True)
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    
    class Meta:
        model = Blog
        fields = ["id", "author","title", "author_name", "image", "description", "created_at", "updated_at"]
        read_only_fields = ["id","author", "created_at", "updated_at"]




class MsPostSerializer(serializers.ModelSerializer):
    # author_name = serializers.StringRelatedField(source="author", read_only=True)
    author_name = serializers.CharField(source="author.full_name", read_only=True)
    class Meta:
        model = MsPost
        fields = ["id", "author", "title", "author_name", "image", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "author",'created_at', 'updated_at']

