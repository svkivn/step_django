from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from blog.forms import PostForm
from blog.models import Post, Category, Tag


################

class PostModelTests(TestCase):

    def setUp(self):
        # Створюємо користувача для тестування
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')


        # Створюємо категорію для посту
        self.category = Category.objects.create(title="Django")

        # Створюємо тег для посту
        self.tag = Tag.objects.create(name='python', slug='python')

    def test_create_post(self):
        """Перевіряємо, чи можна створити пост з валідними даними"""
        post = Post.objects.create(
            title='Test Post',
            author=self.user,
            body='This is a test post.',
            category=self.category,
            status=Post.Status.DRAFT,
        )
        post.tags.add(self.tag)

        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.body, 'This is a test post.')
        self.assertEqual(post.category, self.category)
        self.assertEqual(post.status, Post.Status.DRAFT)
        self.assertIn(self.tag, post.tags.all())  # Перевіряємо чи тег додано до посту
        self.assertEqual(post.slug, 'test-post')  # Перевірка чи slug правильно сформований
        self.assertEqual(post.image, 'default.png')
        self.assertEqual(post.get_absolute_url(), f'/blog/{post.id}/')




class PostCreateTests3(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     super().setUpClass()
    #     # Створюємо користувача і логін через клієнт
    #     cls.user = User.objects.create_user(username='testuser', password='12345')
    #     cls.client_auth = Client()
    #     cls.client_auth.force_login(cls.user)


    def setUp(self):
        # Створюємо користувача для тестування
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

        # Створюємо категорію для посту
        self.category = Category.objects.create(title="Django")

        # Створюємо тег для посту
        self.tag = Tag.objects.create(name='python', slug='python')

        self.form_class = PostForm
        self.template = 'blog/post/create_post.html'

    def test_create_post_get(self):
        """Перевіряємо створення нового поста через GET-запит"""

        url = reverse('blog:create_post')  # URL на сторінку створення поста
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, self.template)
        form = response.context.get('form', None)
        self.assertIsInstance(form, self.form_class)


    def test_create_post(self):
        """Перевіряємо створення нового поста через POST-запит"""

        url = reverse('blog:create_post')  # URL на сторінку створення поста
        data = {
            'title': 'New Post',
            'body': 'This is a new post.',
            'category': self.category.id,
            'status': Post.Status.PUBLISHED,
            'tags': [self.tag.id],
            'publish': '2024-09-30T10:00'
        }

        response = self.client.get(url)
        form = response.context.get('form', None)
        self.assertIsInstance(form, self.form_class)

        response = self.client.post(url, data)
        # # Перевіряємо, чи відбулося перенаправлення після створення поста
        self.assertEqual(response.status_code, 302)
        #
        # # Перевіряємо, чи пост був створений
        self.assertEqual(Post.objects.count(), 1)
        self.assertTrue(Post.objects.filter(title='New Post').exists())  # Заголовок 'New Post'
        # Перевіряємо, чи збережені поля поста
        post = Post.objects.first()
        self.assertEqual(post.title, 'New Post')
        self.assertEqual(post.body, 'This is a new post.')
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.category, self.category)



