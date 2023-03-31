from django.test import TestCase, Client

from recipes.models import Tag, Ingredient
from users.models import User


class URLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.tag = Tag.objects.create(
            name='Завтрак',
            color='#FF8000',
            slug='breakfast'
        )
        cls.ingredient = Ingredient.objects.create(
            name='Вода',
            measurement_unit='мл'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(URLTests.user)

    def test_tags_ingredients(self):
        """
        Проверка доступности ресурсов tags и ingredients.
        Используется неавторизованный пользователь.
        """
        url_name = [
            '/api/tags/',
            f'/api/tags/{URLTests.tag.id}/',
            '/api/ingredients/',
            f'/api/ingredients/{URLTests.ingredient.id}/'
        ]
        for address in url_name:
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertEqual(response.status_code, 200)
                response = self.client.post(address)
                self.assertEqual(response.status_code, 401)

    def test_users(self):
        """Проверка доступности ресурса users."""
        url_name = [
            '/api/users/',
            f'/api/users/{URLTests.user.id}/',
        ]
        for address in url_name:
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertEqual(response.status_code, 200)
        # количество пользователей до созданий нового
        users_before = list(User.objects.values_list('id', flat=True))
        post_data = {
            "email": "test@ya.ru",
            "username": "test",
            "first_name": "test_name",
            "last_name": "test_last_name",
            "password": "!te111st"
        }
        response = self.client.post(
            '/api/users/',
            data=post_data,
            follow=True
        )
        # проверка статуса при создании нового пользователя
        self.assertEqual(response.status_code, 201)
        # проверка увеличения количества пользователей
        self.assertEqual(User.objects.count(), len(users_before) + 1)
        # проверка наличия нового пользователя по переданным параметрам
        self.assertTrue(
            User.objects.filter(
                email=post_data['email'],
                username=post_data['username'],
                first_name=post_data['first_name'],
                last_name=post_data['last_name']
            ).exists()
        )

        post_token_data = {
            'password': post_data['password'],
            'email': post_data['email']
        }
        response = self.client.post(
            '/api/auth/token/login/',
            data=post_token_data,
            follow=True
        )
        # проверка генерации токена
        self.assertEqual(response.status_code, 200)
