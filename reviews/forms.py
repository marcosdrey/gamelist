from django import forms
from django.core.exceptions import ValidationError
from .models import GameReview


def is_integer(value):
    if not isinstance(value, int):
        raise ValidationError('Rating must be an integer.')
    return value


class GameReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=10, validators=[is_integer])

    class Meta:
        model = GameReview
        fields = ('comment', 'rating',)
