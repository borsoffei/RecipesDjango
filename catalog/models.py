from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.template.defaultfilters import truncatechars
from django.utils import timezone





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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_recipes')
    average_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    DIFFICULTY_CHOICES = [
        (1, 'Легкая'),
        (2, 'Средняя'),
        (3, 'Сложная'),
    ]
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)

    # def is_favorite(self, user):
    #     return self.savedrecipe_set.filter(user=user).exists()

    def rating_count(self):
        return self.rating_set.count()

    def calculate_average_rating(self):
        # Получаем все оценки для этого рецепта
        ratings = Rating.objects.filter(recipe=self)

        # Вычисляем среднее значение
        average = ratings.aggregate(Avg('score'))['score__avg']

        # Если нет оценок, вернем None
        if average is None:
            return None

        # Иначе вернем среднее значение, округленное до одного знака после запятой
        return round(average, 1)
    # def short_instructions(self):
    #     return truncatechars(self.instructions, 10)  # обрезает до 10 символов
    #
    # def short_title(self):
    #     return truncatechars(self.title, 10)

    # short_instructions.short_description = 'Short Instructions'  # заголовок колонки в админке
    # short_title.short_description = 'Short Title'
    def __str__(self):
        return truncatechars(self.title, 10)


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Rating(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Сначала сохраняем оценку
        # Затем обновляем средний рейтинг рецепта
        self.recipe.average_rating = self.recipe.calculate_average_rating()
        self.recipe.save()

    def delete(self, *args, **kwargs):
        recipe = self.recipe  # Сохраняем ссылку на рецепт перед удалением оценки
        super().delete(*args, **kwargs)  # Удаляем оценку
        # Обновляем средний рейтинг рецепта
        recipe.average_rating = recipe.calculate_average_rating()
        recipe.save()

    def __str__(self):
        return str(self.recipe) + '-' + str(self.score)


