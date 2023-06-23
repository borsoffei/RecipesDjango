from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RegistrationForm, RecipeForm
from django.contrib.auth import authenticate, login, logout
from .models import Recipe, Category, SavedRecipe, RecipeIngredient, Ingredient
from django.contrib.auth.models import User


# search_query = request.GET.get('search', '')
# filter_query = request.GET.get('filter', '')
# time_query = request.GET.get('time', '')
# sort_query = request.GET.get('sort', '')
#
# recipes = Recipe.objects.all()
#
# if search_query:
#     recipes = recipes.filter(title__icontains=search_query)
# if filter_query:
#     recipes = recipes.filter(ingredients__name=filter_query)
# if time_query:
#     recipes = recipes.filter(time=time_query)
# if sort_query:
#     recipes = recipes.order_by(sort_query)
#
# if not recipes.exists():
#     message = 'No recipes found'
# else:
#     message = ''
# {'recipes': recipes}
# Create your views here.
def index(request):
    return render(request, 'index.html', )


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)  # Don't forget to hash the password
            user.save()
            return redirect('index')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Invalid username or password
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('index')  # предполагая, что у вас есть представление с именем 'index' для главной страницы


@login_required
def profile(request):
    recipes = Recipe.objects.filter(user=request.user)
    return render(request, 'profile.html', {'recipes': recipes})


def user_view(request, username):
    user = User.objects.get(username=username)
    recipes = Recipe.objects.filter(user=user)
    return render(request, 'user.html', {'user': user, 'recipes': recipes})


def favorites_view(request):
    saved_recipes = SavedRecipe.objects.filter(user=request.user)
    return render(request, 'favorites.html', {'saved_recipes': saved_recipes})


def category_view(request, category_name):
    category = Category.objects.get(name=category_name)
    if request.method == 'POST':
        # Get filter data from POST
        sorting = request.POST.get('sorting')
        time = request.POST.getlist('time')
        difficulty = request.POST.getlist('difficulty')
        ingredients = request.POST.getlist('ingredients')

        # Filter recipes based on filter data
        recipes = Recipe.objects.filter(category=category)
        if sorting:
            if 'asc' in sorting:
                order = ''
            else:
                order = '-'
            if 'difficulty' in sorting:
                recipes = recipes.order_by(f'{order}difficulty')
            elif 'time' in sorting:
                recipes = recipes.order_by(f'{order}time')
            elif 'rating' in sorting:
                recipes = recipes.order_by(f'{order}rating')
        if time:
            # Convert time ranges to actual time values
            time_ranges = {
                'up_to_15': (0, 15),
                '15_to_30': (15, 30),
                '30_to_60': (30, 60),
                '60_to_90': (60, 90),
                '90_plus': (90, 10000),
            }
            queries = [Q(time__range=time_ranges[t]) for t in time]
            query = queries.pop()
            for item in queries:
                query |= item
            recipes = recipes.filter(query)
        if difficulty:
            # Convert difficulty levels to actual difficulty values
            difficulty_levels = {
                'easy': 1,
                'normal': 2,
                'hard': 3,
            }
            recipes = recipes.filter(difficulty__in=[difficulty_levels[d] for d in difficulty])
        if ingredients:
            # Get the ingredients by their IDs
            ingredient_objects = Ingredient.objects.filter(id__in=ingredients)
            # Filter the recipes by the ingredients
            recipes = recipes.filter(recipeingredient__ingredient__in=ingredient_objects).distinct()
    else:
        recipes = Recipe.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'recipes': recipes})


def create_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()

            # Get the count of ingredients from the POST data
            ingredientCount = int(request.POST["ingredient_count"])

            # Create RecipeIngredient objects for each selected ingredient
            for i in range(1, ingredientCount + 1):
                ingredient_id = request.POST[f"ingredient_{i}"]
                quantity = request.POST[f"quantity_{i}"]
                ingredient = Ingredient.objects.get(id=ingredient_id)
                RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity)

            return redirect('profile')
    else:
        form = RecipeForm()
        ingredients = Ingredient.objects.all()  # Get all ingredients for the form
    return render(request, 'create_recipe.html', {'form': form, 'ingredients': ingredients})


def recipe_detail_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipe_detail.html', {'recipe': recipe})
