from django.urls import path
from . import views
from .views import ForumView

urlpatterns = [
    path('', ForumView.as_view(), name='forum'),
    path('topic/<int:pk>', views.topic, name='topic'),
    path('topic/<int:pk>/like_topic', views.liked_topic, name="liked_topic"), #Aqui vai ser adc o <int:pk> futuramente
    path('topic/<int:pk>/dislike_topic', views.disliked_topic, name="disliked_topic"), #Aqui vai ser adc o <int:pk> futuramente
    path('topic/<int:pk>/like_comment', views.liked_comment, name="liked_comment"),
    path('topic/<int:pk>/dislike_comment', views.disliked_comment, name="disliked_comment"),
    path('topic/create', views.create_topic, name="create_topic"),
    path('topic/<int:pk>/edit', views.edit_topic, name="edit_topic"),
    path('topic/<int:pk>/delete', views.delete_topic, name="delete_topic"),

]
