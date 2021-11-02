from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.user_without_post = User.objects.create_user(username='NoName')
        cls.authorized_client_without_post = Client()
        cls.authorized_client_without_post.force_login(cls.user_without_post)
        cls.group = Group.objects.create(
            title='testgroup',
            slug='testgroup',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        self.guest_client = Client()

    def test_urls_exists(self):
        response_list = [
            '/',
            '/about/author/',
            '/about/tech/',
            '/group/testgroup/',
            '/profile/auth/',
            '/posts/1/',
        ]
        for field in response_list:
            with self.subTest(field=field):
                self.assertEqual(
                    self.guest_client.get(field).status_code, 200)

    def test_unexisting_url(self):
        self.assertEqual(
            self.guest_client.get(
                '/unexisting_page/').status_code, 404)

    def test_post_edit_url(self):
        self.assertEqual(
            URLTests.authorized_client.get(
                '/posts/1/edit/').status_code, 200)

    def test_post_create_url(self):
        self.assertEqual(
            URLTests.authorized_client_without_post.get(
                '/create/').status_code, 200)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/': 'posts/index.html',
            '/group/testgroup/': 'posts/group_list.html',
            '/profile/auth/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
            '/posts/1/edit/': 'posts/post_form.html',
            '/create/': 'posts/post_form.html'
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
