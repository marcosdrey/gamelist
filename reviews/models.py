from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image


class Game(models.Model):
    title = models.CharField(max_length=200, verbose_name="Título")
    content = models.TextField(max_length=500, verbose_name="Conteúdo")
    game_image = models.ImageField(default="default.jpg", upload_to='games-images', verbose_name="Imagem")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.game_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.game_image.path)

    def average_rating(self):
        ratings = GameReview.objects.filter(game=self)
        if ratings.exists():
            return ratings.aggregate(models.Avg('rating'))['rating__avg']
        return None

    def total_reviews(self):
        reviews = GameReview.objects.filter(game=self)
        if reviews.exists():
            return reviews.count()
        return None

    def __str__(self):
        return self.title


class GameReview(models.Model):
    comment = models.TextField(null=True, blank=True, verbose_name="Comentário")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    likes = models.ManyToManyField(User, related_name='reviews_liked', blank=True, verbose_name="Likes")
    dislikes = models.ManyToManyField(User, related_name='reviews_disliked', blank=True, verbose_name="Dislikes")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews', verbose_name="Game")
    rating = models.IntegerField(
        validators=[MinValueValidator(0, "Nota mínima é 0"),
                    MaxValueValidator(10, "Nota máxima é 10")],
        verbose_name="Avaliação"
    )

    def __str__(self):
        return f"Avaliação de {self.author} em '{self.game}'"
