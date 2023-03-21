from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet, SubscribeView, RecipeViewSet, SubscriptionsView


router = DefaultRouter()
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:user_id>/subscribe/', SubscribeView.as_view()),
    path('users/subscriptions/', SubscriptionsView.as_view())
]

"""
router = DefaultRouter()
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('recipes', RecipeViewSet)
router.register('ingredients', IngredientViewSet)
router.register(
    'recipes/(?P<recipe_id>\\d+)/shopping_cart',
    ShoppingCartViewSet,
    basename='shopping_cart')
router.register(
    'recipes/(?P<recipe_id>\\d+)/favorite',
    FavoriteViewSet,
    basename='favorite')
router.register(
    'users/(?P<user_id>\\d+)/subscribe',
    SubscribeViewSet,
    basename='subscribe')
# роутеры на подписки под вопросом
urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/download_shopping_cart/', download_shopping_cart),
    path('users/subscriptions/', subscriptions),
    path('users/set_password/', set_password),
    path('auth/token/login/', create_token),
    path('auth/token/logout/', remove_token),

    path('ingredients/', IngredientList.as_view()),
    path('ingredients/', IngredientDetail.as_view())
]
"""