from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.messages import add_message, constants
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
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

    def dispatch(self, request, *args, **kwargs):
        topics_by_this_user = Topic.objects.filter(author=request.user).order_by('-date_posted')
        if topics_by_this_user.exists():
            last_topic = topics_by_this_user.first()
            delta = timezone.now() - last_topic.date_posted
            minutes_elapsed = delta.total_seconds() / 60
            if minutes_elapsed < 30:
                add_message(request, constants.WARNING,
                            f"You must wait 30 minutes to create a new topic! (Last one was created {minutes_elapsed:.0f} minute(s) ago).")
                return redirect('forum')
        return super().dispatch(request, *args, **kwargs)

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

    def form_valid(self, form):
        topic = self.get_object()
        if topic.content == form.cleaned_data['content'] and topic.title == form.cleaned_data['title']:
            return redirect('topic', topic.topic.id)
        topic = form.save(commit=False)
        if not topic.is_edited:
            topic.is_edited = True
        topic.date_edited = timezone.now()
        topic.save()
        return super().form_valid(form)


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


class EditReviewView(LoginRequiredMixin, UpdateView):
    model = TopicReview
    template_name = 'edit_review.html'
    context_object_name = 'review'
    form_class = TopicReviewForm

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if review.author == request.user:
            return super().dispatch(request, *args, **kwargs)
        add_message(request, constants.ERROR, "You don't have permission to access this.")
        return reverse_lazy('topic', kwargs={'pk': review.topic.id})

    def get_success_url(self):
        review = self.get_object()
        topic_id = review.topic.id
        return reverse_lazy('topic', kwargs={'pk': topic_id})

    def form_valid(self, form):
        review = self.get_object()
        if review.comment == form.cleaned_data['comment']:
            return redirect('topic', review.topic.id)
        review = form.save(commit=False)
        if not review.is_edited:
            review.is_edited = True
        review.date_edited = timezone.now()
        review.save()
        return super().form_valid(form)


class DeleteReviewView(DeleteView):
    model = TopicReview

    def dispatch(self, request, *args, **kwargs):
        review = self.get_object()
        if request.method == 'POST' and review.author == request.user:
            return super().dispatch(request, *args, **kwargs)
        add_message(request, constants.ERROR, "You don't have permission to access this.")
        return reverse_lazy('topic', kwargs={'pk': review.topic.id})

    def get_success_url(self):
        review = self.get_object()
        topic_id = review.topic.id
        return reverse_lazy('topic', kwargs={'pk': topic_id})


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
