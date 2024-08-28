from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Post, Tag, Rating
from .forms import TagForm, RatingForm


# Create your views here.

def create_tag(request):
    if request.method=="POST":
        form = TagForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            tag = Tag.objects.create(**form.cleaned_data)
            # tag = form.save()
            # tag.slug = tag.name # slugify(test.test_name)
            # tag.save()
            messages.success(request, f"Tag {tag.slug} was created")
            return HttpResponseRedirect(reverse("blog:create-tag"))
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'blog/tag/create_tag.html', {'form': form, "tags": []})
    else:
        form = TagForm()
        tags = Tag.objects.all()
        return render(request, 'blog/tag/create_tag.html', {'form': form, "tags": tags})


"""
Метод form.save() використовується в Django для збереження даних форми в базі даних, 
але він працює лише з формами, які є підкласами ModelForm. 
Якщо ви використовуєте звичайну форму (наприклад, forms.Form), 
вам потрібно вручну створити або оновити об'єкт моделі і зберегти його в базі даних.
"""


def edit_tag(request, pk):
    tag = get_object_or_404(klass=Tag, pk=pk)
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            # tag.name = form.cleaned_data["name"]
            # tag.slug = form.cleaned_data["slug"]
            # tag.save()
            tag = form.save(instance=tag) # need def. method save in form
            messages.success(request, f"Tag {tag.slug} was update")
            return redirect("blog:create-tag")
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, 'blog/tag/create_tag.html', {'form': form, "tags": []})
    else:
        form = TagForm(initial={"name": tag.name, "slug": tag.slug})
        # tags = Tag.objects.all()
        return render(request, 'blog/tag/create_tag.html', {'form': form, "tags": []})


def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        tag.delete()
        messages.success(request, f"Tag {tag.slug} was deleted")
        return redirect("blog:create-tag")
    return render(request, 'blog/tag/delete_tag.html', {"tag": tag, "form": RatingForm()})


def posts_list(request):
    posts = Post.objects.all()
    return render(request, template_name="blog/post/list.html", context={'posts': posts})


def post_cards(request):
    posts = Post.objects.all()
    return render(request, "index.html", {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)

    current_rating = post.ratings.aggregate(Avg('score'))['score__avg'] or 0
    current_rating = int(round(current_rating))  # Округлюємо до найближчого цілого числа

    return render(request, 'blog/post/detail.html', {'post': post, 'current_rating': current_rating, "form": RatingForm()})


def rate_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            score = form.cleaned_data['score']  # Доступ до значення поля 'score'
            print(form.cleaned_data)
            rating, created = Rating.objects.update_or_create(post=post, defaults={'score': score})
            mess_value = "create" if created else "update"
            messages.success(request, f"Rating for {post.title}  with score={rating.score} was {mess_value}")
            return redirect(reverse('blog:post-detail',  kwargs={'id': post_id}))
        else:
            messages.success(request, form.errors)
    else:
        form = RatingForm()
    return render(request, 'blog/post/detail.html', {'post': post, "form": form})



        # return redirect(reverse('blog:post-detail', kwargs={'id': post_id}))

