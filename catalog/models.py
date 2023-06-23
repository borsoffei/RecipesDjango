from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=64)
    instructions = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.IntegerField(default=None)
    DIFFICULTY_CHOICES = [
        (1, 'Легкая'),
        (2, 'Средняя'),
        (3, 'Сложная'),
    ]
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def ingredient_name(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)

    # возможно заменить на просто массив
    def recipe_ingredient(self):
        return {self.recipe: [self.ingredient, self.quantity]}

    def ingredient_recipe(self):
        return {self.ingredient: [self.recipe, self.quantity]}


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Rating(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)