from django.shortcuts import render, get_object_or_404
from .models import Post


# Create your views here.

def posts_list(request):
    posts = Post.objects.all()
    return render(request, template_name="blog/post/list.html", context={'posts': posts})


def post_cards(request):
    posts = Post.objects.all()
    return render(request, "index.html", {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post/detail.html', {'post': post})
