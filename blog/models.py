from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = ('DF', 'Draft')
        PUBLISHED = ('PB', 'Published')

    title = models.CharField(verbose_name="Назва поста", max_length=250)
    body = models.TextField()
    slug = models.SlugField(max_length=250, unique=True)

    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True,
                                 related_name="posts")

    tags = models.ManyToManyField("Tag", related_name='blog_posts')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return f"{self.title} - {self.id}"

    class Meta:
        ordering = ["-publish"]
        verbose_name_plural = "Публікації"
        verbose_name = "Публікація"

    def get_absolute_url(self):
        return reverse('blog:post-detail', args=[self.pk])


class Category(models.Model):
    title = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True, help_text='A label for name tag.')
    slug = models.SlugField(max_length=31, unique=True, help_text='A label for URL config.')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Tags for posts'

    def save(self, *args, **kwargs):
        print("save to db")
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)