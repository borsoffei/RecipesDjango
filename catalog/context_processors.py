from .models import Category, Ingredient


def categories(request):
    return {'categories': Category.objects.all()}


def ingredients(request):
    return {'ingredients': Ingredient.objects.all()}
