from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.messages import add_message, constants
from .models import Game, GameComment, GameRating
from .forms import GameRatingForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.core.paginator import Paginator
from django.views.generic import ListView, View


# Create your views here.

def home(request):
    if request.method == "GET":
        return render(request, 'home.html')
    elif request.method == "POST":
        game_name = request.POST.get('search_game')
        if not game_name:
            return render(request, 'home.html')
        games = Game.objects.filter(title__icontains=game_name)
        games_annotate = games.annotate(total_reviews=Count('gamerating'), avg_rating=Avg('gamerating__rating'))
        games_with_this_name = games_annotate.order_by('-total_reviews', '-avg_rating')
        p = Paginator(games_with_this_name, 3)
        page_number = request.GET.get('page', 1)
        page = p.get_page(page_number)
        return render(request, 'home.html', {'games_with_this_name': games_with_this_name, 'pages': p, 'this_page': page, 'last_search': game_name})

def reviews(request):
    games = Game.objects.annotate(total_reviews=Count('gamerating'), avg_rating=Avg('gamerating__rating'))
    context = {
        'games': games.order_by('-total_reviews', '-avg_rating')[:10]
    }
    return render(request, 'reviews.html', context)

def game_review(request, pk):
    game = get_object_or_404(Game, id=pk)
    comments = GameComment.objects.filter(game=game)
    ratings = GameRating.objects.filter(game=game)
    average_rating = game.average_rating
    try:
        user_already_rated = ratings.get(user=request.user)
    except:
        user_already_rated = None
        pass
    if request.method == "GET":
        gr_form = GameRatingForm(initial={'user': request.user, 'game': game})
        context = {
        'game': game, 
        'gr_form': gr_form, 
        'comments':comments,
        'average_rating':average_rating,
        'ratings':ratings,
    }
        if user_already_rated:
            context['user_already_rated'] = user_already_rated
        return render(request, 'game_review.html', context)
    elif request.method == "POST":
        if 'rating' in request.POST:
            if user_already_rated:
                add_message(request, constants.ERROR, "You've already rated!", extra_tags='comment-rl')
                return redirect('game_review-page', pk)
            rating = request.POST.get('rating')
            user_comment = request.POST.get('user_comment_tarea')
            if user_comment:
                if len(user_comment) > 1500:
                    add_message(request, constants.ERROR, "Your comment shouldn't have more than 1500 characters!", extra_tags='comment-rl')
                    return redirect('game_review-page', pk)
                this_comment = GameComment(author=request.user, content=user_comment, game=game)
                this_comment.save()
            this_rating = GameRating(user=request.user, game=game, rating=rating)
            this_rating.save()
            return redirect('game_review-page', pk)
        else:
            user_already_rated.delete()
            user_comment = GameComment.objects.filter(author=request.user, game=game)
            if user_comment:
                user_comment.delete()
            add_message(request, constants.SUCCESS, "You can rate again!", extra_tags='comment-rl')
            return redirect('game_review-page', pk)
        
@login_required
def game_comment_like(request, pk):
    like = False
    dislike_was_active = False
    if request.method == "POST":
        this_game = get_object_or_404(Game, id=pk)
        comment_id = request.POST['comment_id']
        this_comment = this_game.comments.get(id=comment_id)
        if request.user in this_comment.dislikes.all():
            this_comment.dislikes.remove(request.user)
            dislike_was_active = True
        if request.user in this_comment.likes.all():
            this_comment.likes.remove(request.user)
            like = False
        else:
            this_comment.likes.add(request.user)
            like = True
        data = {
            "liked":like,
            "likes_count":this_comment.likes.all().count(),
            "dislike_was_active":dislike_was_active
        }
        return JsonResponse(data, safe=False)
        
    return redirect(reverse("game_review-page", pk))

@login_required
def game_comment_dislike(request, pk):
    dislike = False
    like_was_active = False
    if request.method == 'POST':
        this_game = get_object_or_404(Game, id=pk)
        comment_id = request.POST['comment_id']
        this_comment = this_game.comments.get(id=comment_id)
        if request.user in this_comment.likes.all():
            this_comment.likes.remove(request.user)
            like_was_active = True
        if request.user in this_comment.dislikes.all():
            this_comment.dislikes.remove(request.user)
            dislike = False
        else:
            this_comment.dislikes.add(request.user)
            dislike = True
        data = {
            "disliked":dislike,
            "dislikes_count":this_comment.dislikes.all().count(),
            "like_was_active": like_was_active
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse("game_review-page", pk))
