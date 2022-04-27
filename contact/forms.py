from .models import Contact
from django import forms

class ContactForm(forms.ModelForm):
    """Форма подписки по email"""
    class Meta:
        model = Contact
        fields = ("email",)
        widgets = {
            "email": forms.TextInput(attrs={"class": "editContent", "placeholder": "Youerr Email..."})
        }
        labels = {
            "email": ''
        }