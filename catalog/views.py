from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from .forms import RegistrationForm, RecipeForm
from django.contrib.auth import authenticate, login, logout
from .models import Recipe, Category, SavedRecipe, RecipeIngredient, Ingredient, Rating, Comment
from django.contrib.auth.models import User


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
    # print(len(list(saved_recipes)))
    recipes = [saved_recipe.recipe for saved_recipe in saved_recipes]
    # for recipe in recipes:
    #     recipe.is_favorite = SavedRecipe.objects.filter(user=request.user, recipe=recipe).exists()
    return render(request, 'favorites.html', {'recipes': recipes})


def category_view(request, category_name):
    category = Category.objects.get(name=category_name)
    sorting = request.POST.get('sorting', [])
    time = request.POST.getlist('time', [])
    difficulty = request.POST.getlist('difficulty', [])
    selected_ingredients = list(map(int, request.POST.getlist('ingredients', [])))
    excluded_ingredients = list(map(int, request.POST.getlist('excluded', [])))
    if request.method == 'GET':

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

        if selected_ingredients:
            # Get the ingredients by their IDs
            ingredient_objects = Ingredient.objects.filter(id__in=selected_ingredients)
            # Filter the recipes by the ingredients
            for ingredient in ingredient_objects:
                recipes = recipes.filter(recipeingredient__ingredient=ingredient)

        if excluded_ingredients:
            # Get the ingredients by their IDs
            excluded_ingredient_objects = Ingredient.objects.filter(id__in=excluded_ingredients)
            # Exclude the recipes that contain the excluded ingredients
            for ingredient in excluded_ingredient_objects:
                recipes = recipes.exclude(recipeingredient__ingredient=ingredient)
    else:
        recipes = Recipe.objects.filter(category=category)
    return render(request, 'category.html', {
        'category': category,
        'recipes': recipes,
        'sorting': sorting,
        'time': time,
        'difficulty': difficulty,
        'selected_ingredients': selected_ingredients,
        'excluded_ingredients': excluded_ingredients,
    })


def create_recipe_view(request):
    ingredients = []
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


def search_view(request):
    query = request.GET.get('q', '')
    recipes = Recipe.objects.filter(Q(title__icontains=query))
    sorting = request.GET.get('sorting', '')
    time = request.GET.getlist('time', [])
    difficulty = request.GET.getlist('difficulty', [])
    selected_ingredients = list(map(int, request.GET.getlist('ingredients', [])))
    excluded_ingredients = list(map(int, request.GET.getlist('excluded', [])))
    selected_category = request.GET.get('category', '')
    if request.method == 'GET':

        # Filter recipes based on filter data
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

        if selected_category:
            recipes = recipes.filter(category=selected_category)

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
            s_query = queries.pop()
            for item in queries:
                s_query |= item
            recipes = recipes.filter(s_query)
        if difficulty:
            # Convert difficulty levels to actual difficulty values
            difficulty_levels = {
                'easy': 1,
                'normal': 2,
                'hard': 3,
            }
            recipes = recipes.filter(difficulty__in=[difficulty_levels[d] for d in difficulty])

        if selected_ingredients:
            # Get the ingredients by their IDs
            ingredient_objects = Ingredient.objects.filter(id__in=selected_ingredients)
            # Filter the recipes by the ingredients
            for ingredient in ingredient_objects:
                recipes = recipes.filter(recipeingredient__ingredient=ingredient)

        if excluded_ingredients:
            # Get the ingredients by their IDs
            excluded_ingredient_objects = Ingredient.objects.filter(id__in=excluded_ingredients)
            # Exclude the recipes that contain the excluded ingredients
            for ingredient in excluded_ingredient_objects:
                recipes = recipes.exclude(recipeingredient__ingredient=ingredient)

    return render(request, 'search.html', {
        'query': query,
        'recipes': recipes,
        'sorting': sorting,
        'time': time,
        'difficulty': difficulty,
        'selected_ingredients': selected_ingredients,
        'excluded_ingredients': excluded_ingredients,
        'selected_category': str(selected_category),
    })


def recipe_detail_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user_rating = None
    comments = Comment.objects.filter(recipe=recipe)
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, recipe=recipe).first()
    if request.method == 'POST':
        comment_text = request.POST.get('comment_making')
        Comment.objects.create(recipe=recipe, text=comment_text, user=request.user)
    return render(request, 'recipe_detail.html', {'recipe': recipe, 'user_rating': user_rating, 'comments': comments, })


def toggle_favorite(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    saved_recipe, created = SavedRecipe.objects.get_or_create(user=request.user, recipe=recipe)
    if not created:
        saved_recipe.delete()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@require_POST
@login_required
def rate_recipe(request, recipe_id):
    score = request.POST.get('score')
    user = request.user
    recipe = Recipe.objects.get(id=recipe_id)

    if recipe.user == user:
        return JsonResponse({'status': 'error', 'message': 'You cannot rate your own recipe.'}, status=200)

    # rating, created = Rating.objects.get_or_create(user=user, recipe=recipe, defaults={'score': score})
    if score == '0':
        # Если score равно 0, удаляем оценку пользователя
        try:
            Rating.objects.filter(user=user, recipe=recipe).delete()
        except Exception as e:
            print(e)
    else:
        # Иначе обновляем или создаем новую оценку
        rating, created = Rating.objects.get_or_create(user=user, recipe=recipe, defaults={'score': score})
        if not created:
            rating.score = score
            rating.save()

    return JsonResponse({'status': 'ok'})
