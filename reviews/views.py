from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.messages import add_message, constants
from .models import Game, GameReview
from .forms import GameReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from django.core.paginator import Paginator
from django.views.generic import ListView, View, DetailView


class HomePage(View):
    def get(self, request, *args, **kwargs):
        search = request.GET.get('search')
        context = {}
        if search:
            games_matched = Game.objects.filter(title__icontains=search)
            if not games_matched.exists():
                return render(request, 'home.html')
            games_matched = games_matched.annotate(avg_rating=Avg('reviews__rating'), total_reviews=Count('reviews'))
            games_ordered = games_matched.order_by('-total_reviews', '-avg_rating')
            p = Paginator(games_ordered, 3)
            page_number = request.GET.get('page', 1)
            this_page = p.get_page(page_number)
            context = {
                'games_founded': games_ordered,
                'pages': p,
                'this_page': this_page
            }
        return render(request, 'home.html', context)


class ReviewsPage(ListView):
    model = Game
    template_name = 'reviews.html'
    context_object_name = 'games'

    def get_queryset(self):
        querysets = super().get_queryset().annotate(avg_rating=Avg('reviews__rating'), 
                                                    total_reviews=Count('reviews'))
        querysets = querysets.order_by('-total_reviews', '-avg_rating')
        if len(querysets) > 10:
            querysets = querysets[:10]
        return querysets


class GameReviewPage(DetailView):
    template_name = "game_review.html"
    model = Game
    context_object_name = "game"

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_already_rated = GameReview.objects.filter(game=self.get_object(), 
                                                      author=request.user).exists()
            if not user_already_rated and 'new_comment' in request.POST:
                form = GameReviewForm(request.POST)
                if form.is_valid():
                    comment = request.POST.get('comment')
                    rating = request.POST.get('rating')
                    review = GameReview(
                        author=request.user,
                        game=self.get_object(),
                        rating=rating
                    )
                    if comment:
                        review.comment = comment
                    review.save()
            elif user_already_rated and 'cancel_comment' in request.POST:
                GameReview.objects.get(game=self.get_object(), author=request.user).delete()
                add_message(request, constants.SUCCESS, "You can rate again!", extra_tags='comment-rl')
        
        return redirect('game_review-page', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = GameReview.objects.filter(game=self.get_object())
        context['comments_count'] = 0
        if reviews.exists():
            context['reviews'] = reviews
            context['comments_count'] = reviews.exclude(comment__isnull=True).count()
            try:
                user_already_rated = reviews.get(author=self.request.user)
                context['user_already_rated'] = user_already_rated
            except:
                pass
            
        context['gr_form'] = GameReviewForm(initial={
            'author': self.request.user,
            'game': self.get_object(),
        })
        return context


@login_required
def game_comment_like(request, pk):
    like = False
    dislike_was_active = False
    if request.method == "POST":
        this_game = get_object_or_404(Game, id=pk)
        review_id = request.POST['comment_id']
        this_review = this_game.reviews.get(id=review_id)
        if request.user in this_review.dislikes.all():
            this_review.dislikes.remove(request.user)
            dislike_was_active = True
        if request.user in this_review.likes.all():
            this_review.likes.remove(request.user)
            like = False
        else:
            this_review.likes.add(request.user)
            like = True
        data = {
            "liked":like,
            "likes_count":this_review.likes.all().count(),
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
        review_id = request.POST['comment_id']
        this_review = this_game.reviews.get(id=review_id)
        if request.user in this_review.likes.all():
            this_review.likes.remove(request.user)
            like_was_active = True
        if request.user in this_review.dislikes.all():
            this_review.dislikes.remove(request.user)
            dislike = False
        else:
            this_review.dislikes.add(request.user)
            dislike = True
        data = {
            "disliked":dislike,
            "dislikes_count":this_review.dislikes.all().count(),
            "like_was_active": like_was_active
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse("game_review-page", pk))
