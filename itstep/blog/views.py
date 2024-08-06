from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Post


def post_list(request):
    # HttpRequest object contains metadata about a request. Like filter items based on a GET parameter.

    q = request.GET.get('q', None)
    if q is None or q is "":
        posts = Post.published.all()
    elif q is not None:
        posts = Post.objects.filter(title__contains=q)

    # render returns an HttpResponse object with the rendered text
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id,
                             status=Post.Status.PUBLISHED)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(request, 'blog/post/detail.html',
                  {'post': post, 'comments': comments, 'form': form})


# def post_detail(request, id):
#     try:
#         post = Post.published.get(id=id)
#     except Post.DoesNotExist:
#         raise Http404("No Post found.")
#     return render(request, 'blog/post/detail.html', {'post':post})


from .forms import EmailPostForm, CommentForm


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method=='POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data  # ... send email
            print(cd)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})


def tags(request, slug=None):
    # With filter function you can return a QuerySet that match lookup parameters
    # You can do lookups through relationships using the double underscore
    posts = Post.objects.filter(tags__slug=slug)
    return render(request, 'blog/post/list.html', {'posts': posts})
