from typing import Any, Dict
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post, Profile
# Create your views here.

class PostListView(ListView):
    model = Post
    paginate_by = 12
    ordering = '-timestamp'
    context_object_name = 'posts'

def search_posts(request):
    keyword = ''
    if request.method == 'POST':
        keyword = request.POST.get('search', '')
        posts = Post.objects.filter(Q(title__icontains=keyword) | Q(text__icontains=keyword) | Q(profile__name__icontains=keyword)).order_by('-timestamp')
        return render(request, 'posts/post_list.html', {'posts': posts, 'keyword': keyword})
    posts = Post.objects.all().order_by('-timestamp')[:12]
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
    posts = Post.objects.filter(profile=profile).order_by('-timestamp')
    return render(request, 'posts/post_list.html', {'posts': posts, 'keyword': profile.name})