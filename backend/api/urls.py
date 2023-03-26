from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, FavoriteView, IngredientViewSet,
                    RecipeViewSet, ShoppingCartView, SubscribeView,
                    SubscriptionsView, TagViewSet)

router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet)
router.register('users', CustomUserViewSet)

urlpatterns = [
    path('recipes/<int:recipe_id>/favorite/', FavoriteView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartView.as_view()),
    path('users/subscriptions/', SubscriptionsView.as_view()),
    path('users/<int:user_id>/subscribe/', SubscribeView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
