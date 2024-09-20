from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from blog.models import Tag


class TagViewTests(TestCase):


    def setUp(self):
        self.tag_data = {
            'name': 'Test Tag2',
            'slug': 'test-tag2',
        }
        self.tag = Tag.objects.create(**self.tag_data)
        super().setUp()

    def tearDown(self):
        Tag.objects.filter(name=self.tag.name).delete()
        super().tearDown()

    def test_create_tag_valid(self):
        tag_data = {'name': 'Test Tag1', 'slug': 'test-tag1', }
        response = self.client.post(reverse('blog:create-tag'), data=tag_data)
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertTrue(Tag.objects.filter(slug='test-tag1').exists())
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Tag test-tag1 was created", messages)

    def test_create_tag_invalid(self):
        invalid_data = {'name': '', 'slug': 'test-tag-inv'}  # Invalid name
        response = self.client.post(reverse('blog:create-tag'), data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Expect to render the form again
        self.assertFalse(Tag.objects.filter(slug='test-tag-inv').exists())
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Please correct the error below.", messages)

    def test_edit_tag_valid(self):
        new_data = {'name': 'Updated Tag', 'slug': 'updated-tag'}
        response = self.client.post(reverse('blog:edit-tag', args=[self.tag.pk]), data=new_data)
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.tag.refresh_from_db()
        self.assertEqual(self.tag.name, 'updated tag') # to_lower
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Tag "updated-tag" was updated.', messages)

    def test_edit_tag_invalid(self):
        invalid_data = {'name': '', 'slug': 'updated-tag'}  # Invalid name
        response = self.client.post(reverse('blog:edit-tag', args=[self.tag.pk]), data=invalid_data)
        self.assertEqual(response.status_code, 200)  # Expect to render the form again
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertNotIn('Tag "updated-tag" was updated.', messages)

    def test_delete_tag(self):
        response = self.client.post(reverse('blog:delete-tag', args=[self.tag.pk]))
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertFalse(Tag.objects.filter(pk=self.tag.pk).exists())
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Tag test-tag2 was deleted", messages)

    def test_delete_tag_not_found(self):
        response = self.client.post(reverse('blog:delete-tag', args=[999]))  # Non-existing tag
        self.assertEqual(response.status_code, 404)  # Expect a 404 error


