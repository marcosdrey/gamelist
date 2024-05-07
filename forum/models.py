from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='comments_liked', blank=True, default=0)
    dislikes = models.ManyToManyField(User, related_name='comments_disliked', blank=True, default=0)
    


class Topic(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='topic_liked', blank=True)
    dislikes = models.ManyToManyField(User, related_name='topic_disliked', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)

class TopicComment(Comment):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='comments')
    def save(self, *args, **kwargs):
        if self.pk:
            old_comment = TopicComment.objects.get(pk=self.pk)
            if old_comment.likes.count() == self.likes.count():
                return super().save(*args, **kwargs)
        return super().save(*args, **kwargs)