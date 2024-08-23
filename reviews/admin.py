from django.contrib import admin
from .models import Game, GameReview


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'game_image')
    search_fields = ('title',)


@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'game', 'rating')
    search_fields = ('game',)
    sortable_by = ('rating',)
