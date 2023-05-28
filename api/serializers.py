from rest_framework import serializers
from books.models import Book
from posts.models import Post, Profile

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    profile_name = serializers.CharField(source='profile.name', read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'profile', 'title', 'text', 'image', 'profile_name', 'timestamp', 'book',)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'