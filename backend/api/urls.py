from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagViewSet, IngredientViewSet,
                    SubscribeView, RecipeViewSet,
                    SubscriptionsView, FavoriteView, ShoppingCartView, CustomUserViewSet)


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet)
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/favorite/', FavoriteView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartView.as_view()),
    path('users/subscriptions/', SubscriptionsView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:user_id>/subscribe/', SubscribeView.as_view()),
]
