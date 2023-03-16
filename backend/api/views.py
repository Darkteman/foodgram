from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view, action
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from recipes.models import Tag, Ingredient
from .serializers import TagSerializer, IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer



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
