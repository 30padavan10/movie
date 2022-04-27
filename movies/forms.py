# from snowpenguin.django.recaptcha3.fields import ReCaptchaField

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
    #captcha = ReCaptchaField() # c джанго 4 не работает

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')  # 'captcha')
        # до добавляения ReCaptcha форма была html, но т.к. добавляем поле 'captcha' то по SOLID данную форму нужно будет рендерить
        # и чтобы сохранились стили которые использовали раннее в форме нужно добавить виджеты, тогда джанго отрендерит
        # форму с нужными нам классами
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border"})
        }