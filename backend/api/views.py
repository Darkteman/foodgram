from datetime import date

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from recipes.models import (Tag, Ingredient, Subscribe, Recipe,
                            Favorite, ShoppingCart, AmountIngredient)
from users.models import User
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeCreateUpdateSerializer,
                          SubscribeSerializer, ShortRecipeSerializer)
from .permissions import IsAuthorOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для рецептов."""
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Вывод файла с консолидированным количеством ингредиентов."""
        user = request.user
        if not user.shopping.exists():
            return Response('В корзине нет товаров')
        shopping_list = 'Foodgram\nИнгредиенты из списка покупок:\n\n'
        ingredients = AmountIngredient.objects.filter(
            recipe__shopping__user=user).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            Sum('amount')).order_by('ingredient__name')
        for item in ingredients:
            shopping_list += (f"{item['ingredient__name']} - "
                              f"{item['amount__sum']} "
                              f"{item['ingredient__measurement_unit']}\n")
        shopping_list += f'\nДата формирования: {date.today()}'
        response = HttpResponse(shopping_list, content_type='text/plain')
        filename = 'shopping_cart.txt'
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для тэгов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class SubscribeView(APIView):
    """Подписка на автора рецепта."""
    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if author != request.user:
            return create_relations(request, author, Subscribe,
                                    SubscribeSerializer, 'author')
        return Response({"errors": "Самому на себя подписаться нельзя!"},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        return delete_relations(request, user_id, User, Subscribe, 'author')


class FavoriteView(APIView):
    """Добавление рецепта в избранное."""
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return create_relations(request, recipe, Favorite,
                                ShortRecipeSerializer, 'recipe')

    def delete(self, request, recipe_id):
        return delete_relations(request, recipe_id,
                                Recipe, Favorite, 'recipe')


class ShoppingCartView(APIView):
    """Добавление рецепта в список покупок."""
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return create_relations(request, recipe, ShoppingCart,
                                ShortRecipeSerializer, 'recipe')

    def delete(self, request, recipe_id):
        return delete_relations(request, recipe_id,
                                Recipe, ShoppingCart, 'recipe')


def create_relations(request, obj, related_model, name_serializer, field):
    """Универсальная функция для создания связей между моделями."""
    kwargs = record_kwargs(request, obj, field)
    created_obj, created = related_model.objects.get_or_create(**kwargs)
    if created:
        serializer = name_serializer(obj, context={'request': request})
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)
    return Response({"errors": "Связь уже существует!"},
                    status=status.HTTP_400_BAD_REQUEST)


def delete_relations(request, id, model, related_model, field):
    """Универсальная функция для удаления связей между моделями."""
    obj = get_object_or_404(model, id=id)
    kwargs = record_kwargs(request, obj, field)
    try:
        related_model.objects.get(**kwargs).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response({"errors": "Отсутствует предварительная связь!"},
                        status=status.HTTP_400_BAD_REQUEST)


def record_kwargs(request, obj, field):
    """Формирование словаря для передачи в менеджер модели."""
    kwargs = {}
    kwargs['user'] = request.user
    kwargs[field] = obj
    return kwargs


class SubscriptionsView(generics.ListAPIView):
    """Вывод списка подписок пользователя."""
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(subscribers__user=self.request.user)
