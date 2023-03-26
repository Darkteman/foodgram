from datetime import date

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import (AmountIngredient, Favorite, Ingredient, Recipe,
                            ShoppingCart, Subscribe, Tag)
from users.models import User

from .filters import RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateUpdateSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          SubscribeSerializer, TagSerializer)
from .utils import create_relations, delete_relations


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Представление для рецептов.
    Фильтрация по автору, тегам, нахождению в избранном и списке покупок.
    Через download_shopping_cart можно скачать txt список покупок.
    """
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Вывод файла с консолидированным количеством ингредиентов."""
        user = request.user
        # оставлять обработку пустой корзины?
        # в тз не требуется, но по сути надо бы)
        if not user.shopping.exists():
            return Response('В корзине нет товаров!')
        shopping_list = 'Foodgram\nСписок покупок:\n\n'
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
    """
    Представление для ингредиентов.
    Поиск по первому вхождению в поле name.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [SearchFilter]
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для тегов.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class SubscribeView(APIView):
    """
    Подписка на автора рецепта.
    """
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
    """
    Добавление рецепта в избранное.
    """
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return create_relations(request, recipe, Favorite,
                                ShortRecipeSerializer, 'recipe')

    def delete(self, request, recipe_id):
        return delete_relations(request, recipe_id,
                                Recipe, Favorite, 'recipe')


class ShoppingCartView(APIView):
    """
    Добавление рецепта в список покупок.
    """
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return create_relations(request, recipe, ShoppingCart,
                                ShortRecipeSerializer, 'recipe')

    def delete(self, request, recipe_id):
        return delete_relations(request, recipe_id,
                                Recipe, ShoppingCart, 'recipe')


class SubscriptionsView(generics.ListAPIView):
    """
    Вывод списка подписок пользователя.
    """
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(subscribers__user=self.request.user)


class CustomUserViewSet(UserViewSet):
    """
    Расширеное представление по UserViewSet Djoser'а.
    Используется для переопределения прав доступа
    к эндпоинту /me/.
    """
    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
