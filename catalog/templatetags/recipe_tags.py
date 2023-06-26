from django import template

register = template.Library()


@register.filter
def is_favorite(recipe, user):
    fav = user.favorite_recipes.all()
    return recipe in fav


# @register.filter
# def average_rating(recipe):
#     return recipe.average_rating()


@register.filter
def rating_count(recipe):
    return recipe.rating_count()
