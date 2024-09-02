from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib import messages

from .models import Post, Tag
from django.db.models import F


def post_list_cards(request):
    posts = Post.published.all()
    posts = Post.objects.annotate(num_comments=Count('comments'))
    # posts = Post.objects.values('title', 'body', 'publish', category_rename=F('category__title'))
    # posts = Post.objects.annotate(num_comments=Count('comments')).select_related("category__title")
    return render(request, 'blog/post/index.html', {'posts': posts})


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
    # post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    # List of active comments for this post
    # comments = post.comments.filter(active=True)

    # updated query 1
    # Завантажуємо пост разом із коментарями заздалегідь
    post = get_object_or_404(Post.objects.select_related("author", "category").prefetch_related('comments', "tags"),
                             id=id)
    # Оскільки коментарі вже завантажені, немає потреби виконувати додатковий запит
    comments = post.comments.all()

    # updated query 2
    # active_comments = Prefetch('comments', queryset=Comment.objects.filter(active=True))
    # post = get_object_or_404(Post.objects.prefetch_related(active_comments), id=id)

    # Form for users to comment
    form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form})


# def post_detail(request, id):
#     try:
#         post = Post.published.get(id=id)
#     except Post.DoesNotExist:
#         raise Http404("No Post found.")
#     return render(request, 'blog/post/detail.html', {'post':post})


from .forms import EmailPostForm, CommentForm, PostForm


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
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
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
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


from . import forms


def create_tag(request):
    if request.method=="POST":
        form = forms.TagForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            tag = form.save(commit=False)
            # tag.slug = tag.name # slugify(test.test_name)
            tag.save()
            messages.success(request, f"Tag {tag.slug} was created")
            return HttpResponseRedirect(reverse("blog:create-tag"))
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'blog/post/edit_tag.html', {'form': form, "tags": []})
    else:
        form = forms.TagForm()
        tags = Tag.objects.all()
        return render(request, 'blog/post/edit_tag.html', {'form': form, "tags": tags})


def edit_tag(request, pk=None):
    '''
    get_object_or_404 raises an Http404 exception and returns a standard 404
    (page not found) error page if the object matching the lookup parameters (pk=pk) is not found.
    '''
    tag = get_object_or_404(Tag, pk=pk)

    if request.method=="POST":
        form = forms.TagForm(data=request.POST, instance=tag)
        # instance keyword argument allows us to update an existing object with
        # form.save() method and populate the form with an existing data for editing.
        if form.is_valid():
            updated_tag = form.save()
            messages.success(request, 'Tag "{}" was updated.'.format(updated_tag.slug))
            return redirect("blog:edit-tag", tag.pk)
        else:
            tags = []
            return render(request, 'blog/post/edit_tag.html', {'form': form, "tags": tags})
    else:
        form = forms.TagForm(instance=tag)  # from obj to form
        tags = Tag.objects.all()
        return render(request, 'blog/post/edit_tag.html', {'form': form, "tags": tags})


def delete_tag(request, pk=None):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    messages.success(request, f"Tag {tag.slug} was deleted")
    # delete() returns how many objects were deleted and how many
    # deletions were executed by object type: (1, {'blog.Tag': 1})
    return redirect("blog:create-tag")


from . import forms


def manage_tag(request, pk=None):
    if pk:
        tag = get_object_or_404(Tag, pk=pk)
    else:
        tag = None

    if request.method=="POST":
        form = forms.TagForm(request.POST, instance=tag)
        if form.is_valid():
            tag = form.save(commit=False)
            if not pk:  # Only set the slug if it's a new tag
                # tag.slug = tag.name # Uncomment and set slug if necessary
                pass
            tag.save()
            if pk:
                messages.success(request, f'Tag "{tag.slug}" was updated.')
            else:
                messages.success(request, f'Tag "{tag.slug}" was created.')
            return HttpResponseRedirect(reverse("blog:manage-tag", args=[tag.pk]))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = forms.TagForm(instance=tag)

    tags = Tag.objects.all()
    return render(request, 'blog/post/edit_tag.html', {'form': form, 'tags': tags})

#######################################
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Не забувайте про request.FILES для завантаження файлів
        if form.is_valid():
            post = form.save(commit=False)  # Не зберігайте ще в базі даних
            post.author = request.user  # Встановлюємо автора поста
            post.save()  # Тепер зберігаємо пост
            form.save_m2m()  # Зберігаємо ManyToMany поля, якщо є
            messages.success(request, f'Post "{post.title}" was created.', extra_tags='bold')
            return redirect('blog:post_detail', post.id)  # Перенаправлення на деталі поста  #
        else:
            messages.error(request, 'Please correct the error below.')
            form.add_error(None, "non-errors")
    else:
        form = PostForm()
    return render(request, 'blog/post/create_post.html', {'form': form})


def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user  # Встановлюємо автора поста
            post.save()
            form.save_m2m()
            messages.success(request, f'Post "{post.title}" was updated.')
            form.send_email(request, msg = f'Post "{post.title}" was updated.')

            return redirect('blog:post_detail', post.id)
        else:
            messages.error(request, 'Please correct the error below.')
            form.add_error(None, "non-errors")
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post/create_post.html', {'form': form, 'post': post})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        messages.success(request, f'Post "{post.title}" was deleted.')
        return redirect('blog:post_list')  # Перенаправлення на список постів
    return render(request, 'post_detail.html', {'post': post})