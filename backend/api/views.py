from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS

from recipes.models import Tag, Ingredient, Subscribe, Recipe
from users.models import User
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeCreateUpdateSerializer, CustomUserSerializer, SubscribeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для рецептов."""
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
    """Осуществление подписки(отписки) на(от) автора рецепта."""
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


class SubscriptionsView(APIView):
    def get(self, request):




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
