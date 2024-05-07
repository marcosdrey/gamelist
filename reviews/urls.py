from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reviews/', views.reviews, name='reviews-page'),
    path('reviews/game/<int:pk>', views.game_review, name='game_review-page'),
    path('reviews/game/<int:pk>/comment-like', views.game_comment_like, name='game_review_comment_like'),
    path('reviews/game/<int:pk>/comment-dislike', views.game_comment_dislike, name='game_review_comment_dislike'),

]
