from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


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

    def is_favorite(self, user):
        return self.savedrecipe_set.filter(user=user).exists()

    def rating_count(self):
        return self.rating_set.count()

    def average_rating(self):
        # Получаем все оценки для этого рецепта
        ratings = Rating.objects.filter(recipe=self)

        # Вычисляем среднее значение
        average = ratings.aggregate(Avg('score'))['score__avg']

        # Если нет оценок, вернем None
        if average is None:
            return None

        # Иначе вернем среднее значение, округленное до одного знака после запятой
        return round(average, 1)

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=200)

    def __str__(self):
        return str(self.recipe) + '-' + str(self.ingredient)


class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Rating(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.recipe) + '-' + str(self.score)


class SavedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + '-' + str(self.recipe)
