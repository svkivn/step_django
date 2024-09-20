from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from blog.models import Post
from http import HTTPStatus


class HomepageTest(TestCase):
    def setUp(self) -> None:
        self.post1 = baker.make(Post, make_m2m=True)
        self.post2 = baker.make(Post, make_m2m=True)
        ps = baker.make(Post, _quantity=3, make_m2m=True)

    def test_homepage_returns_correct_response(self):
        response = self.client.get(reverse("blog:post_list"))

        self.assertTemplateUsed(response, 'blog/post/list.html')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_returns_post_list(self):
        posts = Post.objects.all()
        self.assertEqual(len(posts), 5)

        response = self.client.get(reverse("blog:post_list_cards"))
        # Отримуємо пости з контексту
        posts = response.context.get('posts', [])
        # Перевіряємо, що пости є в контексті
        self.assertEqual(len(posts), 5)
        # чи відображаються на сторінці
        self.assertContains(response, self.post1.title.title())

