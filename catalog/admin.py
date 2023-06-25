from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import Recipe, Rating, RecipeIngredient, Ingredient, Category, Comment


# Register your models here.


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'short_instructions', 'category', 'user', 'time', 'created_at', 'updated_at', 'difficulty')
    date_hierarchy = 'created_at'
    filter_horizontal = ('favorited_by',)
    list_filter = ('title', 'category', 'user', 'time', 'difficulty')
    fields = ['title', 'instructions', ('time', 'category', 'difficulty')]
    def short_instructions(self, obj):
        return truncatechars(obj.instructions, 10)  # обрезает до 10 символов

    short_instructions.short_description = 'Short Instructions'  # заголовок колонки в админке

admin.site.register(Recipe, RecipeAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('score', 'user', 'recipe')


admin.site.register(Rating, RatingAdmin)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')


admin.site.register(RecipeIngredient, RecipeIngredientAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Ingredient, IngredientAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'recipe', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'


admin.site.register(Comment, CommentAdmin)
