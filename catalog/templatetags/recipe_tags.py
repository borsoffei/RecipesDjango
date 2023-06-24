from django import template

register = template.Library()

@register.filter
def is_favorite(recipe, user):
    return recipe.is_favorite(user)