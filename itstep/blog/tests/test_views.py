from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve

from blog.views import post_list


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('blog:post_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post/list.html')

    def test_home_url_resolves_home_view(self):
        # перевірка відповідності запитуваної URL-адреси зі списком URL-адрес, перерахованих у модулі urls.py
        view = resolve('/blog/')
        self.assertEquals(view.func, post_list)

    def test_home_view_template(self):
        """Перевірка, чи використовує сторінка правильний шаблон"""
        url = reverse('blog:post_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/post/list.html')  # Замініть на правильний шлях до шаблону

    def test_home_page_contains_correct_html(self):
        url = reverse('blog:post_list')
        response = self.client.get(url)
        self.assertContains(response, '<h1>My Blog</h1>')


