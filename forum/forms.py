from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Topic, TopicReview


TITLE_MIN_LENGTH = 10
TITLE_MAX_LENGTH = 100

TOPIC_MIN_LENGTH = 10
TOPIC_MAX_LENGTH = 1000

COMMENT_MIN_LENGTH = 10
COMMENT_MAX_LENGTH = 500


class TopicForm(forms.ModelForm):
    title = forms.CharField(
        validators=[
            MinLengthValidator(TITLE_MIN_LENGTH,
                               f"Title must be at least {str(TITLE_MIN_LENGTH)} characters long."),
            MaxLengthValidator(TITLE_MAX_LENGTH,
                               f"Title must have a maximum of {TITLE_MAX_LENGTH} characters")
        ]

    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your topic here'}),
        validators=[
            MinLengthValidator(TOPIC_MIN_LENGTH,
                               f"Content must be at least {str(TOPIC_MIN_LENGTH)} characters long."),
            MaxLengthValidator(TOPIC_MAX_LENGTH,
                               f"Content must have a maximum of {str(TOPIC_MAX_LENGTH)} characters.")
        ]
    )

    class Meta:
        model = Topic
        fields = ('title', 'content')


class TopicReviewForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Write your comment here'}),
        validators=[
            MinLengthValidator(COMMENT_MIN_LENGTH,
                               f"Comment must be at least {str(COMMENT_MIN_LENGTH)} characters long."),
            MaxLengthValidator(COMMENT_MAX_LENGTH,
                               f"Comment must have a maximum of {str(COMMENT_MAX_LENGTH)} characters.")
        ]
    )

    class Meta:
        model = TopicReview
        fields = ('comment',)
