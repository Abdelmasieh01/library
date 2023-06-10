from rest_framework import serializers
from books.models import Book, Borrowing
from posts.models import Post, Profile

class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='get_category_display', read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'category', 'code', 'name', 'author', 'copies', 'available', 'category_name')

class PostSerializer(serializers.ModelSerializer):
    profile_name = serializers.CharField(source='profile.name', read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'profile', 'title', 'text', 'image', 'profile_name', 'timestamp', 'book',)

class ProfileSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = Profile
        fields = '__all__'

    def to_representation(self, instance):
        id = instance.id
        user = instance.user.id
        photo = instance.photo
        name = instance.name()

        data = {
                'id': id,
                'user': user,
                'photo': photo,
                'name': name
            }

        return data
    
class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__'