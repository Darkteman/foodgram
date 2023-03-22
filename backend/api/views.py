from datetime import date

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from recipes.models import Tag, Ingredient, Subscribe, Recipe, Favorite, ShoppingCart, AmountIngredient
from users.models import User
from .serializers import (TagSerializer, IngredientSerializer,
                          RecipeSerializer, RecipeCreateUpdateSerializer,
                          CustomUserSerializer, SubscribeSerializer,
                          ShortRecipeSerializer)
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
    """Подписка(отписка) на(от) автора рецепта."""
    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if author != request.user:
            subscription, created = Subscribe.objects.get_or_create(
                user=request.user,
                author=author
            )
            if created:
                serializer = SubscribeSerializer(author,
                                                 context={'request': request})
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({"errors": "Подписка уже существует!"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"errors": "Самому на себя подписаться нельзя!"},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        try:
            Subscribe.objects.get(
                user=request.user,
                author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"errors": "Предварительной подписки не было!"},
                            status=status.HTTP_400_BAD_REQUEST)


class FavoriteView(APIView):
    """Добавление рецепта в избранное."""
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if created:
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response({"errors": "Рецепт уже в избранном!"},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            Favorite.objects.get(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"errors": "Рецепт не был в избранном!"},
                            status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartView(APIView):
    """Добавление рецепта в список покупок."""
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        shopping_cart, created = ShoppingCart.objects.get_or_create(
            user=request.user,
            recipe=recipe
        )
        if created:
            serializer = ShortRecipeSerializer(recipe)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response({"errors": "Рецепт уже в списке покупок!"},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            ShoppingCart.objects.get(
                user=request.user,
                recipe=recipe
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"errors": "Рецепт не был в списке покупок!"},
                            status=status.HTTP_400_BAD_REQUEST)


class SubscriptionsView(generics.ListAPIView):
    """Вывод списка подписок пользователя."""
    serializer_class = SubscribeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(subscribers__user=self.request.user)


# return Response({'message': f'Удаляю подписку с пользователем {user_id}'})


# class IngredientViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Ingredient.objects.all()
#         serializer = IngredientSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = IngredientSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def retrieve(self, request, pk):
#         ingredient = Ingredient.objects.get(pk=pk)
#         serializer = IngredientSerializer(ingredient)
#         return Response(serializer.data)


# class IngredientListAPI(APIView):

#     def get(self, request):
#         ingredients = Ingredient.objects.all()
#         serializer = IngredientSerializer(ingredients, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = IngredientSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

# class IngredientDetailAPI(APIView):

#     def get(self, request, pk):
#         ingredient = Ingredient.objects.get(pk=pk)
#         serializer = IngredientSerializer(ingredient)
#         return Response(serializer.data)
