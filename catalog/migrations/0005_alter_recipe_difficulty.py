# Generated by Django 4.2.2 on 2023-06-22 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_alter_recipe_difficulty_alter_recipe_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='difficulty',
            field=models.IntegerField(choices=[(1, 'Легкая'), (2, 'Средняя'), (3, 'Сложная')]),
        ),
    ]
