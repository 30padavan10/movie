from .models import Rating_star, Rating, Reviews
from django import forms


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(queryset=Rating_star.objects.all(), widget=forms.RadioSelect(), empty_label=None)
    # чтобы выводить список доступных звезд переопределяем поле star

    class Meta:
        model = Rating
        fields = ("star",)


class ReviewForm(forms.ModelForm):
    """Формы отзывов"""
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')