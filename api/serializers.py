from rest_framework import serializers
from books.models import Book, Borrowing, Recommendation, Announcement
from posts.models import Post, Profile


class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source='get_category_display', read_only=True)
    age_category_name = serializers.CharField(
        source='get_age_category_display', read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'category', 'code', 'name', 'author',
                  'copies', 'available', 'category_name', 'age_category_name', 'link', 'image')


class PostSerializer(serializers.ModelSerializer):
    profile_name = serializers.CharField(source='profile.name', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'profile', 'title', 'text', 'image',
                  'profile_name', 'timestamp', 'book',)


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
    book_age_category = serializers.CharField(
        source='book.age_category', read_only=True)
    book_image = serializers.URLField(source='book.image', read_only=True)

    class Meta:
        model = Recommendation
        fields = ('id', 'book_name', 'title', 'book_author', 'book_category_name',
                  'book_category', 'book_code', 'book_age_category', 'book_image', 
                  'text', 'book', 'timestamp')

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

#Serializing the link to the app
class AppLinkSerializer(serializers.Serializer):
    data = {
            'version': 100,
            'link': '',
        }