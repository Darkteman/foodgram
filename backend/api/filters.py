from django_filters.rest_framework import FilterSet, filters

from recipes.models import Recipe


class RecipeFilter(FilterSet):
    """
    Фильтрация рецептов.
    По автору, тегам, нахождению в избранном и списке покупок.
    """
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_is_in_shopping')
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def filter_is_in_shopping(self, queryset, name, value):
        if value:
            return queryset.filter(shopping__user=self.request.user)
        return queryset


def recipes_limit(request, obj):
    """
    Ограничение количества выводимых рецептов.
    Используется при выводе подписок пользователя.
    """
    limit = request.query_params.get('recipes_limit')
    if limit:
        recipes = obj.recipes.all()[:int(limit)]
    else:
        recipes = obj.recipes.all()
    return recipes
