from django.contrib import admin
from .models import Recipe, Rating, RecipeIngredient, SavedRecipe, Ingredient, Category, Comment
# Register your models here.
admin.site.register(Recipe)
admin.site.register(Rating)
admin.site.register(RecipeIngredient)
admin.site.register(SavedRecipe)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(Comment)