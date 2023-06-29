from rest_framework import serializers
from books.models import Book, Borrowing, Recommendation, Announcement
from posts.models import Post, Profile
from django.conf import settings


class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='get_category_display', read_only=True)
    subcategory = serializers.SerializerMethodField()

    def get_subcategory(self, instance):
        return instance.subcategory.values_list('title')

    class Meta:
        model = Book
        fields = ('id', 'category', 'code', 'name', 'author',
                  'copies', 'available', 'category_name', 'subcategory', 'link', 'image')


class PostSerializer(serializers.ModelSerializer):
    profile_name = serializers.CharField(source='profile.name', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'profile', 'title', 'text', 'image',
                  'profile_name', 'timestamp', 'book',)


class ProfileSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, instance):
        return f'https://stpeterlibrary.crabdance.com/media/{instance.photo}' 

    class Meta:
        model = Profile
        fields = ('id', 'name', 'photo', 'user')


class BorrowingSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.name', read_only=True)
    borrower_name = serializers.CharField(
        source='borrower.name', read_only=True)

    class Meta:
        model = Borrowing
        fields = ('id', 'book_name', 'borrow_date', 'return_date',
                  'returned', 'borrower', 'borrower_name', 'book_id')


class RecommendationSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source='book.name', read_only=True)
    book_author = serializers.CharField(source='book.author', read_only=True)
    book_category_name = serializers.CharField(
        source='book.get_category_display', read_only=True)
    book_category = serializers.CharField(
        source='book.category', read_only=True)
    book_code = serializers.CharField(source='book.code', read_only=True)
    book_image = serializers.URLField(source='book.image', read_only=True)



    class Meta:
        model = Recommendation
        fields = ('id', 'book_name', 'title', 'book_author', 'book_category_name',
                  'book_category', 'book_code', 'book_image', 'text', 'book', 'timestamp')

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

#Serializing the link to the app
class AppLinkSerializer(serializers.Serializer):
    data = {
            'version': '1.0.0',
            'link': 'https://drive.google.com/file/d/1fq5npWfyX9o-tdZSAPsPrpdwAhEXJa1p/view?usp=drive_link',
        }