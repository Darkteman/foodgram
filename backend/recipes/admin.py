from django.contrib import admin

from .models import (Tag, Ingredient, Recipe,
                     AmountIngredient, Favorite, ShoppingCart, Subscribe)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class AmountIngredientInline(admin.TabularInline):
    model = AmountIngredient
    min_num = 1
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    list_filter = ('name', 'author', 'tags')
    inline = (AmountIngredientInline,)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(AmountIngredient)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
