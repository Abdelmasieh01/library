from .serializers import BookSerializer, PostSerializer, ProfileSerializer
from books.models import Book
from posts.models import Post, Profile
from django.db.models import Q
from rest_framework import generics
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

class BookAPIView(generics.ListAPIView):   
    serializer_class = BookSerializer

    def get_queryset(self):
        queryset = Book.objects.all().order_by('category', 'code')
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(Q(name__icontains=search) | Q(author__icontains=search))

        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category=int(category))
        
        return queryset

class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'profile__name']

@api_view(['GET'])
def get_profile(request):
    if request.query_params:
        pk = request.query_params.get('pk')
        try:
            profile = Profile.objects.get(pk=int(pk))
            item = ProfileSerializer(profile)
            return Response(item.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

