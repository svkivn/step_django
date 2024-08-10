from django.test import TestCase
from django.urls import reverse, resolve

from .views import post_list


class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('blog:post_list')
        print(url)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        # перевірка відповідності запитуваної URL-адреси зі списком URL-адрес, перерахованих у модулі urls.py
        view = resolve('/blog/')
        self.assertEquals(view.func, post_list)




