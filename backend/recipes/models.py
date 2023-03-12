from django.db import models
from django.contrib.auth import get_user_model #временно пока нет модели юзера

User = get_user_model()


class Tag(models.Model):
    """Модель для описания Тэга."""
    name = models.CharField('Название тега', max_length=100)
    color = models.CharField('Цвет', max_length=7)
    slug = models.SlugField('Сокращенное название', unique=True, max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Ingredient(models.Model):
    """Модель для описания Ингредиента."""
    name = models.TextField('Название ингредиента', max_length=200)
    measurement_unit = models.CharField('Единицы измерения', max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.MOdel):
    """Модель для описания Рецепта."""
    name = models.TextField('Название рецепта', max_length=200)
    text = models.TextField('Описание', max_length=3000)
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')
    image = models.ImageField('Изображение')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиент'
        #что-то тут надо расширить для указания количества ингредиентов
    )