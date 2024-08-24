from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.messages import add_message, constants
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Topic, TopicReview
from .forms import TopicForm, TopicReviewForm


class ForumView(ListView):
    model = Topic
    template_name = 'forum.html'
    context_object_name = 'topics'
    ordering = ['-date_posted', '-likes']
    paginate_by = 5


class TopicView(DetailView):
    model = Topic
    template_name = 'topic.html'
    context_object_name = 'topic'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            form = TopicReviewForm(request.POST)
            if form.is_valid():
                comment = request.POST.get('comment')
                review = TopicReview(
                    author=request.user,
                    topic=self.get_object(),
                    comment=comment
                )
                review.save()

            else:
                request.session['review_form_data'] = request.POST
                request.session['form_errors'] = form.errors.as_json()
        return redirect('topic', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = TopicReview.objects.filter(topic=self.get_object())
        if reviews.exists():
            context['reviews'] = reviews.order_by('-likes')

        review_form_data = self.request.session.pop('review_form_data', None)
        form_errors = self.request.session.pop('form_errors', None)

        if review_form_data:
            context['review_form'] = TopicReviewForm(review_form_data)
            if form_errors:
                context['form_errors'] = form_errors
        else:
            context['review_form'] = TopicReviewForm(initial={
                'author': self.request.user,
                'topic': self.get_object()
            })

        context['comments_count'] = reviews.exclude(comment__isnull=True).count()
        return context


class CreateTopicView(LoginRequiredMixin, CreateView):
    model = Topic
    template_name = 'create_topic.html'
    context_object_name = 'topic'
    form_class = TopicForm

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('topic', kwargs={'pk': self.object.pk})


class EditTopicView(LoginRequiredMixin, UpdateView):
    model = Topic
    template_name = 'edit_topic.html'
    context_object_name = 'topic'
    form_class = TopicForm

    def dispatch(self, request, *args, **kwargs):
        topic = self.get_object()
        if topic.author == request.user:
            return super().dispatch(request, *args, **kwargs)
        add_message(request, constants.ERROR, "You don't have permission to access this.")
        return redirect('forum')

    def get_success_url(self):
        return reverse_lazy('topic', kwargs={'pk': self.object.pk})


class DeleteTopicView(LoginRequiredMixin, DeleteView):
    model = Topic
    template_name = 'delete_topic.html'
    context_object_name = 'topic'
    success_url = reverse_lazy('forum')

    def dispatch(self, request, *args, **kwargs):
        topic = self.get_object()
        if topic.author == request.user:
            return super().dispatch(request, *args, **kwargs)
        add_message(request, constants.ERROR, "You don't have permission to access this.")
        return redirect('forum')


@login_required
def liked_topic(request, pk):
    like = False
    dislike_was_active = False
    if request.method == "POST":
        topic_id = request.POST['topic_id']
        this_topic = get_object_or_404(Topic, id=topic_id)
        if request.user in this_topic.dislikes.all():
            this_topic.dislikes.remove(request.user)
            dislike_was_active = True
        if request.user in this_topic.likes.all():
            this_topic.likes.remove(request.user)
            like = False
        else:
            this_topic.likes.add(request.user)
            like = True
        data = {
            "liked": like,
            "likes_count": this_topic.likes.all().count(),
            "dislike_was_active": dislike_was_active
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('topic', kwargs={'pk': pk}))


@login_required
def disliked_topic(request, pk):
    dislike = False
    like_was_active = False
    if request.method == 'POST':
        topic_id = request.POST['topic_id']
        this_topic = get_object_or_404(Topic, id=topic_id)
        if request.user in this_topic.likes.all():
            this_topic.likes.remove(request.user)
            like_was_active = True
        if request.user in this_topic.dislikes.all():
            this_topic.dislikes.remove(request.user)
            dislike = False
        else:
            this_topic.dislikes.add(request.user)
            dislike = True
        data = {
            "disliked": dislike,
            "dislikes_count": this_topic.dislikes.all().count(),
            "like_was_active": like_was_active
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('topic', kwargs={'pk': pk}))


@login_required
def liked_comment(request, pk):
    like = False
    dislike_was_active = False
    if request.method == "POST":
        comment_id = request.POST['comment_id']
        this_comment = TopicReview.objects.get(id=comment_id)
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
            "liked": like,
            "likes_count": this_comment.likes.all().count(),
            "dislike_was_active": dislike_was_active
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('topic', kwargs={'pk': pk}))


@login_required
def disliked_comment(request, pk):
    dislike = False
    like_was_active = False
    if request.method == 'POST':
        comment_id = request.POST['comment_id']
        this_comment = TopicReview.objects.get(id=comment_id)
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
            "disliked": dislike,
            "dislikes_count": this_comment.dislikes.all().count(),
            "like_was_active": like_was_active
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('topic', kwargs={'pk': pk}))
