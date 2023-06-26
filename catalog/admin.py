from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import Recipe, Rating, RecipeIngredient, Ingredient, Category, Comment


# Register your models here.


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'short_title', 'short_instructions', 'category', 'user', 'time', 'created_at', 'updated_at', 'difficulty',
        'average_rating')
    list_display_links = ('short_title',)
    date_hierarchy = 'created_at'
    filter_horizontal = ('favorited_by',)
    list_filter = ('category', 'user', 'time', 'difficulty', 'average_rating')
    fields = ['title', 'instructions', ('time', 'category', 'difficulty', 'average_rating')]
    search_fields = ('title',)
    def short_instructions(self, obj):
        return truncatechars(obj.instructions, 10)  # обрезает до 10 символов

    def short_title(self, obj):
        return truncatechars(obj.title, 10)

    short_instructions.short_description = 'Instructions'  # заголовок колонки в админке
    short_title.short_description = 'Title'

admin.site.register(Recipe, RecipeAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('score', 'user', 'recipe')
    list_filter = ('score', 'user', 'recipe')
    list_display_links = ('score',)
    fields = ('user', 'recipe', 'score')



admin.site.register(Rating, RatingAdmin)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'recipe', 'ingredient')
    list_filter = ('quantity', 'recipe', 'ingredient')
    list_display_links = ('quantity',)


admin.site.register(RecipeIngredient, RecipeIngredientAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Ingredient, IngredientAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(Category, CategoryAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'recipe', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_filter = ('user', 'recipe')
    list_display_links = ('text',)
    search_fields = ('text',)


admin.site.register(Comment, CommentAdmin)
