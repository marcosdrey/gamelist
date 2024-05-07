from django import forms
from .models import GameRating
from django.core.exceptions import ValidationError

def is_integer(value):
    if isinstance(value, float):
        if value.is_integer():
            return value
        else:
            raise ValidationError('Rating must be an integer.')
    elif not isinstance(value, int):
        raise ValidationError('Rating must be an integer.')
    return value
            

class GameRatingForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=10, validators=[is_integer])

    class Meta:
        model = GameRating
        fields = ('rating',)