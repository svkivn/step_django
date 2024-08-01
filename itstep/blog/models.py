from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = ('DF', 'Draft')
        PUBLISHED = ('PB', 'Published')

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)

    # Using CASCADE, you specify that when the referenced user is deleted,
    # the database will also delete all related blog posts.
    # related_name to specify the name of the reverse relationship, from User to Post,
    # using the user.blog_posts notation
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField( )

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # We can access Post.Status.choices to obtain the available choices, Post.Status.labels to obtain
    # the human-readable names, and Post.Status.values to obtain the actual values of the choices.
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title
