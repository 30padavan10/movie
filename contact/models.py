from django.db import models

# Create your models here.

class Contact(models.Model):
    """Подписка на email"""
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True) # auto_now_add - создается при создании записи и не меняется
                                                    # auto_now - обновляется при изменении записи в бд

    def __str__(self):
        return self.email