from django import template

register = template.Library()
from movies.models import Category, Movie


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()

# если требуется вставить большой блок html кода на несколько страниц
# на странице куда вставляется используется {% load movie_tag %} и {% get_last_movies count=1 %}
@register.inclusion_tag('movies/tags/last_movies.html')  # путь до соответствующего блока
def get_last_movies(count):
    """5 последних фильмов"""
    movies = Movie.objects.order_by("id")[:count]
    return {"last_movies": movies}