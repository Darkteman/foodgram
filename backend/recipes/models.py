from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Tag(models.Model):
    """
    Модель для описания Тега.
    """
    name = models.CharField('Название тега', unique=True, max_length=200)
    color = models.CharField('Цвет', max_length=7)
    slug = models.SlugField('Сокращенное название',
                            unique=True, max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Модель для описания Ингредиента.
    """
    name = models.TextField('Название ингредиента', max_length=200)
    measurement_unit = models.CharField('Единицы измерения', max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement'
            )
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    """
    Модель для описания Рецепта.
    """
    name = models.TextField('Название рецепта', max_length=200)
    text = models.TextField('Описание', max_length=3000)
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления (мин.)',
        validators=[MinValueValidator(
            1, message='Время должно быть больше 1 минуты!'
        )]
    )
    # image = models.TextField('Изображение', blank=True, null=True)
    # Временно, поле сделано текстом и может быть не заполнено
    image = models.ImageField('Изображение', upload_to='recipes/images/')
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
        through='AmountIngredient',
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class AmountIngredient(models.Model):
    """
    Промежуточная модель для указания количества ингредиентов.
    """
    recipe = models.ForeignKey(
        Recipe,
        related_name='amounts',
        verbose_name='Рецепт',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='amounts',
        verbose_name='Ингредиент',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(
            1, message='Количество должно быть больше 1!'
        )]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return (f'"{self.recipe.name}": {self.ingredient.name} '
                f'- {self.amount} {self.ingredient.measurement_unit}')


class Favorite(models.Model):
    """
    Модель для создания связи рецепт - избранное.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.recipe} добавлен в избранное пользователем {self.user}'


class ShoppingCart(models.Model):
    """
    Модель для создания связи рецепт - корзина покупок.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Рецепт в продуктовой корзине'
        verbose_name_plural = 'Рецепты в продуктовой корзине'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]

    def __str__(self):
        return f'{self.recipe} добавлен в список пользователем {self.user}'


class Subscribe(models.Model):
    """
    Модель для оформления подписки на автора.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscribe'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на пользователя {self.author}'
