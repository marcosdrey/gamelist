from django.contrib import admin
from .models import Game, GameComment, GameRating

admin.site.register(Game)
admin.site.register(GameComment)
admin.site.register(GameRating)

