from typing import Any, Dict
from django.urls import reverse
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, CharField, Value
from django.db.models.functions import Concat
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Profile
from .forms import PostForm
# Create your views here.

class PostListView(ListView):
    model = Post
    paginate_by = 12
    ordering = '-timestamp'
    context_object_name = 'posts'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(approved=True)

def search_posts(request):
    keyword = ''
    if request.method == 'POST':
        keyword = request.POST.get('search', '')
        posts = Post.objects.filter(approved=True).annotate(
            name=Concat(
                'profile__user__first_name',
                Value(' '),
                'profile__user__last_name',
                output_field=CharField())).filter(Q(title__icontains=keyword) | Q(text__icontains=keyword) | Q(name__icontains=keyword)).order_by('-timestamp')
        return render(request, 'posts/post_list.html', {'posts': posts, 'keyword': keyword})
    posts = Post.objects.filter(approved=True).order_by('-timestamp')[:12]
    return render(request, 'posts/post_list.html', {'posts': posts, 'keyword': keyword})

class PostDetailView(DetailView):
    model = Post
    template_name_suffix = '_detail'
    context_object_name = 'post'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().exclude(pk=self.get_object().pk).order_by('-timestamp')[:3]
        return context
    
def posts_by_profile(request, pk=1):
    profile = get_object_or_404(Profile, pk=pk)
    posts = Post.objects.filter(profile=profile, approved=True).order_by('-timestamp')
    return render(request, 'posts/post_list.html', {'posts': posts, 'keyword': profile.__str__})

'''
class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/admin/login/'
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'
    def get_success_url(self):
        return reverse('books:create-post',)
'''

@login_required(login_url='/web_auth/login/')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            profile = request.user.profile
            title = form.cleaned_data['title']
            text = form.cleaned_data['text']
            book = form.cleaned_data['book']
            image = form.cleaned_data['image']
            post = Post(title=title, text=text, profile=profile)
            if book is not None and book != '':
                post.book = book
            if image is not None and image != '':
                post.image = image
            post.save()
            return render(request, 'posts/post_form.html', {'form': form, 'success': True})
        else:
            return render(request, 'posts/post_form.html', {'form': form, 'error': True})
    form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})
    