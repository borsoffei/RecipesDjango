from django import template

register = template.Library()


@register.filter
def is_favorite(recipe, user):
    return recipe.is_favorite(user)


@register.filter
def average_rating(recipe):
    return recipe.average_rating()


@register.filter
def rating_count(recipe):
    return recipe.rating_count()
