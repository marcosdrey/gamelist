from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título")
    content = models.TextField(max_length=1000, verbose_name="Conteúdo")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Autor")
    likes = models.ManyToManyField(User, related_name='topic_liked', blank=True, verbose_name="Likes")
    dislikes = models.ManyToManyField(User, related_name='topic_disliked', blank=True, verbose_name="Dislikes")
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name="Data Postada")
    is_edited = models.BooleanField(default=False, verbose_name="Editado")
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name="Data Editada")

    def __str__(self):
        return self.title


class TopicReview(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_review', verbose_name="Autor")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='reviews', verbose_name="Tópico")
    comment = models.TextField(null=True, blank=True, verbose_name="Comentário")
    likes = models.ManyToManyField(User, related_name='topic_reviews_liked', blank=True, verbose_name="Likes")
    dislikes = models.ManyToManyField(User, related_name='topic_reviews_disliked', blank=True, verbose_name="Dislikes")
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name="Data Postada")
    is_edited = models.BooleanField(default=False, verbose_name="Editado")
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name="Data Editada")

    def __str__(self):
        return f"Avaliação de {self.author} em '{self.topic}'"
