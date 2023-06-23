from django import forms
from django.contrib.auth.models import User
from .models import Recipe


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class RecipeForm(forms.ModelForm):
    time = forms.IntegerField(
        widget=forms.NumberInput(attrs={'min': '5', 'step': '5'}),
        required=True

    )
    DIFFICULTY_CHOICES = [
        ('', '-------'),
        (1, 'Легкая'),
        (2, 'Средняя'),
        (3, 'Сложная'),

    ]

    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        widget=forms.Select,
        required = True
    )

    title = forms.CharField(
        widget=forms.Textarea(attrs={ 'maxlength': '64'}),
        required=True
    )

    class Meta:
        model = Recipe
        fields = ['title', 'instructions', 'category', 'time', 'difficulty']
        required = "__all__"
