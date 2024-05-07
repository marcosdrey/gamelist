from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    game_image = models.ImageField(default="default.jpg", upload_to='games-images')
    def save(self, *args, **kwargs):    
        super().save(*args, **kwargs)
        img = Image.open(self.game_image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.game_image.path)
    
    def average_rating(self):
        ratings = GameRating.objects.filter(game=self)
        if ratings.exists():
            return ratings.aggregate(models.Avg('rating'))['rating__avg']
        return None
    
    def total_reviews(self):
        reviews = GameRating.objects.filter(game=self)
        if reviews.exists():
            return reviews.count()
        return None

    

class GameComment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='game_comments_liked', blank=True, default=0)
    dislikes = models.ManyToManyField(User, related_name='game_comments_disliked', blank=True, default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='comments')

class GameRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    