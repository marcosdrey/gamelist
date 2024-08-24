from django.urls import path
from . import views

urlpatterns = [
    path('', views.ForumView.as_view(), name='forum'),
    path('topic/<int:pk>/', views.TopicView.as_view(), name='topic'),
    path('topic/create/', views.CreateTopicView.as_view(), name='create_topic'),
    path('topic/<int:pk>/edit/', views.EditTopicView.as_view(), name="edit_topic"),
    path('topic/<int:pk>/delete/', views.DeleteTopicView.as_view(), name="delete_topic"),


    path('topic/<int:pk>/like_topic', views.liked_topic, name="liked_topic"),
    path('topic/<int:pk>/dislike_topic', views.disliked_topic, name="disliked_topic"),
    path('topic/<int:pk>/like_comment', views.liked_comment, name="liked_comment"),
    path('topic/<int:pk>/dislike_comment', views.disliked_comment, name="disliked_comment"),
]
