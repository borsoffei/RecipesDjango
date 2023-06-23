from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('category/<str:category_name>/', views.category_view, name='category_view'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('user/<str:username>/', views.user_view, name='user_view'),
    path('favorites/', views.favorites_view, name='favorites_view'),
    path('create_recipe/', views.create_recipe_view, name='create_recipe'),
    path('recipe/<int:recipe_id>/', views.recipe_detail_view, name='recipe_detail'),
]