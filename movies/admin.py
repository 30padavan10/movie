from django.contrib import admin

from .models import Actor, Category, Genre, Movie, Reviews, Rating, Rating_star, MovieShots


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "movie", "ip")

admin.site.register(Actor)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Reviews)

#admin.site.register(Rating)
admin.site.register(Rating_star)
admin.site.register(MovieShots)
