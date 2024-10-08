# Generated by Django 5.0.4 on 2024-08-22 21:33

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_remove_gamerating_game_remove_gamerating_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamereview',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='gamereview',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='reviews_disliked', to=settings.AUTH_USER_MODEL, verbose_name='Dislikes'),
        ),
        migrations.AlterField(
            model_name='gamereview',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.game', verbose_name='Game'),
        ),
        migrations.AlterField(
            model_name='gamereview',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='reviews_liked', to=settings.AUTH_USER_MODEL, verbose_name='Likes'),
        ),
        migrations.AlterField(
            model_name='gamereview',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, 'Nota mínima é 0'), django.core.validators.MaxValueValidator(10, 'Nota máxima é 10')], verbose_name='Avaliação'),
        ),
    ]
