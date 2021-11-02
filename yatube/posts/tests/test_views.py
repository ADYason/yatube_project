from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Noname')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group = Group.objects.create(
            title='testgroup',
            slug='testgroup',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post1 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post2 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post3 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post4 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post5 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post6 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post7 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post8 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post9 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post10 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post11 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )
        cls.post12 = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group
        )

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'testgroup'}):
            'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'Noname'}):
            'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': '1'}):
            'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/post_form.html',
            reverse('posts:post_edit', kwargs={'post_id': '1'}):
            'posts/post_form.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = PostsPagesTests.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_context(self):
        response = PostsPagesTests.authorized_client.get(
            reverse('posts:index'))
        post_list = response.context.get('post_list')
        self.assertEqual(str(post_list), str(Post.objects.all()))

    def test_group_posts_context(self):
        response = PostsPagesTests.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'testgroup'}))
        post_list = response.context.get('post_list')
        group = response.context.get('group')
        self.assertEqual(str(post_list), str(group.posts.all()))

    def test_profile_context(self):
        response = PostsPagesTests.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'Noname'}))
        post_list = response.context.get('post_list')
        profile = response.context.get('profile')
        self.assertEqual(str(post_list), str(profile.author.all()))

    def test_post_detail_context(self):
        response = PostsPagesTests.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': '1'}))
        post = response.context.get('post')
        post_id = response.context.get('post_id')
        self.assertEqual(str(post), str(Post.objects.get(id=post_id)))

    def test_post_create_context(self):
        response = PostsPagesTests.authorized_client.get(
            reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_context(self):
        response = PostsPagesTests.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': '1'}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)
        post = response.context.get('post')
        post_id = response.context.get('post_id')
        self.assertEqual(str(post), str(Post.objects.get(id=post_id)))

    def test_paginator_first_page(self):
        response_list = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'testgroup'}),
            reverse('posts:profile', kwargs={'username': 'Noname'}),
        ]
        for rev in response_list:
            with self.subTest(rev=rev):
                response = PostsPagesTests.authorized_client.get(rev)
                self.assertEqual(len(response.context['page_obj']), 10)

    def test_paginator_second_page(self):
        response_list = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'testgroup'}),
            reverse('posts:profile', kwargs={'username': 'Noname'}),
        ]
        for rev in response_list:
            with self.subTest(rev=rev):
                response = PostsPagesTests.authorized_client.get(
                    rev + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 3)

    def test_new_post_appears(self):
        response_list = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': 'testgroup'}),
            reverse('posts:profile', kwargs={'username': 'Noname'}),
        ]
        for rev in response_list:
            with self.subTest(rev=rev):
                response = PostsPagesTests.authorized_client.get(rev)
                first_object = response.context['page_obj'][0]
                post_author_0 = first_object.author
                post_text_0 = first_object.text
                post_group_0 = first_object.group
                self.assertEqual(str(post_author_0), 'Noname')
                self.assertEqual(post_text_0, 'Текст')
                self.assertEqual(str(post_group_0), 'testgroup')
