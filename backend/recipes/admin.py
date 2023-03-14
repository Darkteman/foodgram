from django.contrib import admin

from .models import (Tag, Ingredient, Recipe,
                     AmountIngredient, Favorite, ShoppingCart, Subscribe)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe)
admin.site.register(AmountIngredient)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(Subscribe)
