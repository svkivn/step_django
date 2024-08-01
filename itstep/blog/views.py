from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    posts = Post.published.all( )

    # render returns an HttpResponse object with the rendered text
    return render(request, 'blog/post/list.html', {'posts':posts})


def post_detail(request, id):
    post = get_object_or_404(Post,
                             id=id, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post': post})



# def post_detail(request, id):
#     try:
#         post = Post.published.get(id=id)
#     except Post.DoesNotExist:
#         raise Http404("No Post found.")
#     return render(request, 'blog/post/detail.html', {'post':post})
