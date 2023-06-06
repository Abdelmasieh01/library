from .serializers import BookSerializer, PostSerializer, ProfileSerializer
from books.models import Book
from posts.models import Post, Profile
from django.db.models import Q,  CharField, Value
from django.db.models.functions import Concat
from rest_framework import generics
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


class ZeroIndexedPagePagination(PageNumberPagination):
    page_size = 10

    def get_page_number(self, request, paginator):
        page_number = super().get_page_number(request, paginator)
        return int(page_number) + 1


class BookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    pagination_class = ZeroIndexedPagePagination

    def get_queryset(self):
        queryset = Book.objects.all().order_by('category', 'code')
        search = self.request.query_params.get('search')
        if search is not None and search != "":
            search_var1 = search.replace('ا', 'أ')
            search_var2 = search.replace('ي', 'ى')
            search_var3 = search_var2.replace('ا', 'أ')
            queryset = queryset.filter(Q(name__icontains=search) | Q(
                author__icontains=search) | Q(name__icontains=search_var1) | Q(author__icontains=search_var1) | Q(name__icontains=search_var2) | Q(author__icontains=search_var2) | Q(name__icontains=search_var3) | Q(author__icontains=search_var3))

        category = self.request.query_params.get('category')
        if (category is not None) and (category != "") and (category != " "):
            queryset = queryset.filter(category=int(category))

        return queryset


class PostAPIView(generics.ListAPIView):
    pagination_class = ZeroIndexedPagePagination
    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-timestamp')
        search = self.request.query_params.get('search')
    
        if search is not None and search != "":
            queryset = queryset.annotate(
                    name=Concat(
                    'profile__user__first_name',
                    Value(' '),
                    'profile__user__last_name',
                    output_field=CharField())).filter(Q(name__icontains=search))
        return queryset


@api_view(['GET'])
def get_book(request):
    if request.query_params:
        pk = request.query_params.get('pk')
        try:
            book = Book.objects.get(pk=int(pk))
            item = BookSerializer(book)
            return Response(item.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_post(request):
    if request.query_params:
        pk = request.query_params.get('pk')
        try:
            post = Post.objects.get(pk=int(pk))
            item = PostSerializer(post)
            return Response(item.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


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
