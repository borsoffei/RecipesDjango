from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import Recipe, Rating, RecipeIngredient, Ingredient, Category, Comment


# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'recipe', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_filter = ('user', 'recipe')
    list_display_links = ('text',)
    search_fields = ['text', 'recipe__title', 'user__username']
    readonly_fields = ('user', 'recipe')


admin.site.register(Comment, CommentAdmin)


class CommentInline(admin.TabularInline):
    model = Comment


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'score', 'user', 'recipe')
    list_filter = ('score', 'user', 'recipe')
    list_display_links = ('score',)
    fields = ('user', 'recipe', 'score')
    search_fields = ('user__username', 'recipe__title')
    readonly_fields = ('user', 'recipe')

admin.site.register(Rating, RatingAdmin)


class RatingInline(admin.TabularInline):
    model = Rating


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'quantity', 'recipe', 'ingredient')
    list_filter = ('quantity', 'recipe', 'ingredient')
    list_display_links = ('id',)
    search_fields = ('recipe__title',)
    readonly_fields = ('quantity', 'recipe', 'ingredient')


admin.site.register(RecipeIngredient, RecipeIngredientAdmin)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'short_title', 'short_instructions', 'category', 'user', 'time', 'created_at', 'updated_at', 'difficulty',
        'average_rating')
    list_display_links = ('short_title',)
    date_hierarchy = 'created_at'
    filter_horizontal = ('favorited_by',)
    list_filter = ('category', 'user', 'time', 'difficulty', 'average_rating')
    fields = ['title', 'user', 'instructions', ('time', 'category', 'difficulty', 'average_rating')]
    search_fields = ('id', 'title', 'user__username')
    readonly_fields = ('average_rating', 'user')
    def short_instructions(self, obj):
        return truncatechars(obj.instructions, 10)  # обрезает до 10 символов

    def short_title(self, obj):
        return truncatechars(obj.title, 10)

    short_instructions.short_description = 'Instructions'  # заголовок колонки в админке
    short_title.short_description = 'Title'
    inlines = [RatingInline, CommentInline, RecipeIngredientInline, ]


admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)


admin.site.register(Ingredient, IngredientAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('id', 'name',)


admin.site.register(Category, CategoryAdmin)
