from rest_framework import serializers
from recipes.models import (Tag, Ingredient, Subscribe, Recipe,
                            AmountIngredient, Favorite, ShoppingCart)

from djoser.serializers import UserCreateSerializer, UserSerializer

from users.models import User


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для модели User.
    Используется при создании пользователя.
    """
    class Meta:
        model = User
        fields = ('email', 'username',
                  'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    """
    Сериализатор для модели User.
    Используется при выводе информации о пользователе.
    """
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated
                and Subscribe.objects.filter(user=user, author=obj).exists())


class ShortRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Recipe.
    Используется при выводе краткой информации о рецепте.
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(CustomUserSerializer):
    """
    Расширенный сериализатор на основе CustomUserSerializer.
    Добавляет рецепты привязанные к автору.
    Используется при выводе информации в подписках.
    """
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        else:
            recipes = obj.recipes.all()
        return ShortRecipeSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Tag.
    Используется при выводе информации о "тэге".
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Ingredient.
    Используется при выводе информации об ингредиенте.
    """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class AmountIngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Ingredient.
    Используется при выводе информации об ингредиенте.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = AmountIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Recipe.
    Используется при выводе информации о рецепте.
    """
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = AmountIngredientSerializer(read_only=True,
                                             many=True, source='amounts')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart',
                  'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated
                and Favorite.objects.filter(user=user,
                                            recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated
                and ShoppingCart.objects.filter(user=user,
                                                recipe=obj).exists())


class AmountIngredientSerializer(serializers.ModelSerializer):
    """
    Промежуточный сериализатор для модели AmountIngredient.
    Связывает ингредиент (по id) и соответсвующее ему количество.
    """
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = AmountIngredient
        fields = ('id', 'amount')


class RecipeCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Recipe.
    Используется при вводе и редактировании информации о рецепте.
    """
    ingredients = AmountIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')

    def validate(self, data):
        ingredients = data.get('ingredients')
        ingredients_unique = []
        for ingredient in ingredients:
            id = ingredient.get('id')
            if id in ingredients_unique:
                raise serializers.ValidationError({
                    'ingredients': 'Ингредиенты не должны повторяться!'})
            ingredients_unique.append(id)
        return data

    @staticmethod
    def create_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            AmountIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        context = {'request': self.context.get('request')}
        return RecipeSerializer(instance, context=context).data
