from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Topic, TopicComment
from django.views.generic import ListView
from django.contrib.messages import add_message, constants
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
class ForumView(ListView):
    model = Topic
    template_name = 'forum.html'
    context_object_name = 'topics'
    ordering = ['-likes']
    paginate_by = 5

def topic(request, pk):
    this_topic = get_object_or_404(Topic, id=pk)
    if request.method == 'GET':
        comments = this_topic.comments.all().order_by('-likes')
        return render(request, 'topic.html', {'topic': this_topic, 'comments': comments})
    elif request.method == 'POST':
        ##COMMENTS FORM
        if 'user_comment_tarea' in request.POST:
            text = request.POST.get('user_comment_tarea')
            if len(text) >= 1500:
                add_message(request, constants.ERROR, "Your comment shouldn't has more than 1500 characters!", extra_tags='comment-rl')
                return redirect('topic', pk)
            topic_comment = TopicComment(topic=this_topic, content=text, author=request.user)
            topic_comment.save()
            return redirect('topic', pk)

@login_required
def create_topic(request):
    if request.method == "GET":
        old_title = request.session.get('old_title')
        old_content = request.session.get('old_content')
        return render(request, 'create_topic.html', {'old_title': old_title, 'old_content': old_content})
    elif request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if len(content) > 3000: 
            add_message(request, constants.WARNING, "Topic's content shouldn't has more than 3000 characters!")
            request.session['old_title'] = title
            request.session['old_content'] = content
            return redirect('create_topic')
        old_title = request.session.pop('old_title', None)
        old_content = request.session.pop('old_content', None)
        new_topic = Topic(title=title, content=content, author=request.user)
        new_topic.save()
        return redirect('topic', new_topic.id)

@login_required
def edit_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    if request.user != topic.author:
        add_message(request, constants.ERROR, "You don't have access to this page.")
        return redirect('forum')
    else:
        if request.method == 'GET':
            return render(request, 'edit_topic.html', {'topic': topic})
        elif request.method == "POST":
            title = request.POST.get('title')
            content = request.POST.get('content')
            if len(content) > 3000: 
                add_message(request, constants.WARNING, "Topic's content shouldn't has more than 3000 characters!")
                return redirect('edit_topic', pk)
            topic.title = title
            topic.content = content
            topic.save()
            add_message(request, constants.SUCCESS, "Topic edited successfully!", extra_tags='topic-rl')
            return redirect('topic', pk)


def delete_topic(request, pk):
    topic = Topic.objects.get(id=pk)
    if request.user != topic.author:
        add_message(request, constants.ERROR, "You don't have access to this page.")
        return redirect('forum')
    else:
        if request.method == 'GET':
            return render(request, 'delete_topic.html', {'topic': topic})
        elif request.method == "POST":
            topic.delete()
            add_message(request, constants.SUCCESS, "Topic deleted successfully!")
            return redirect('forum')
        

@login_required
def liked_topic(request, pk):
    like=False
    dislike_was_active=False
    if request.method == "POST":
        topic_id=request.POST['topic_id']
        this_topic=get_object_or_404(Topic, id=topic_id)
        if request.user in this_topic.dislikes.all():
            this_topic.dislikes.remove(request.user)
            dislike_was_active = True
        if request.user in this_topic.likes.all():
            this_topic.likes.remove(request.user)
            like=False
        else:
            this_topic.likes.add(request.user)
            like=True
        data={
            "liked":like,
            "likes_count":this_topic.likes.all().count(),
            "dislike_was_active":dislike_was_active
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse('topic', pk))

@login_required
def disliked_topic(request, pk):
    dislike=False
    like_was_active=False
    if request.method == 'POST':
        topic_id=request.POST['topic_id']
        this_topic=get_object_or_404(Topic, id=topic_id)
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
            "disliked":dislike,
            "dislikes_count": this_topic.dislikes.all().count(),
            "like_was_active": like_was_active
        }
        return JsonResponse(data, safe=False)
    return redirect(reverse("topic", pk))

@login_required
def liked_comment(request, pk):
    like = False
    dislike_was_active = False
    if request.method == "POST":
        this_topic = get_object_or_404(Topic, id=pk)
        comment_id = request.POST['comment_id']
        this_comment = this_topic.comments.get(id=comment_id)
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
    return redirect(reverse("topic", pk))

@login_required
def disliked_comment(request, pk):
    dislike = False
    like_was_active = False
    if request.method == 'POST':
        this_topic = get_object_or_404(Topic, id=pk)
        comment_id = request.POST['comment_id']
        this_comment = this_topic.comments.get(id=comment_id)
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
    return redirect(reverse("topic", pk))