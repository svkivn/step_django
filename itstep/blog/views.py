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


from .forms import EmailPostForm


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data # ... send email
            print(cd)
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
                      {'post': post, 'form': form, 'sent': sent})
