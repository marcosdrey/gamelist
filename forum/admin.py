from django.contrib import admin
from .models import Topic, TopicReview


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'content', 'show_likes', 'show_dislikes', 'date_posted')
    search_fields = ('title',)
    sortable_by = ('show_likes', 'show_dislikes', 'date_posted')

    def show_likes(self, obj):
        return sum(obj.likes.all())

    def show_dislikes(self, obj):
        return sum(obj.dislikes.all())

    show_likes.short_description = 'Likes'
    show_dislikes.short_description = 'Dislikes'


@admin.register(TopicReview)
class TopicReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'topic', 'show_likes', 'show_dislikes', 'comment')
    search_fields = ('topic',)
    sortable_by = ('show_likes', 'show_dislikes')

    def show_likes(self, obj):
        return sum(obj.likes.all())

    def show_dislikes(self, obj):
        return sum(obj.dislikes.all())

    show_likes.short_description = 'Likes'
    show_dislikes.short_description = 'Dislikes'
