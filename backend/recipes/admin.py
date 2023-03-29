from django.contrib import admin

from .models import (AmountIngredient, Favorite, Ingredient, Recipe,
                     ShoppingCart, Subscribe, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class AmountIngredientInline(admin.TabularInline):
    model = AmountIngredient


class TagsInLine(admin.TabularInline):
    model = Recipe.tags.through


class RecipeAdmin(admin.ModelAdmin):

    def added_to_favorites_amount(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    added_to_favorites_amount.short_description = 'Добавлений в избранное'

    list_display = ('id', 'name', 'author', 'added_to_favorites_amount')
    list_filter = ('name', 'author', 'tags')
    inlines = (AmountIngredientInline, TagsInLine,)
    exclude = ('tags',)
    readonly_fields = ('added_to_favorites_amount',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
