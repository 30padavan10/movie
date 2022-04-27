from modeltranslation.translator import register, TranslationOptions
from .models import Category, Actor, Movie, Genre, MovieShots


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ("name", "description")  # те поля которые участвуют в переводе
    # Данное приложение добавит к нашим моделям поля для перевода
    # после этого выполняем
    # makemigrations и migrate
    # если проект новый этого достаточно, если уже существуют записи в БД, то еще выполнить
    # update_translation_fields


@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ("name", "description")


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ("title", "tagline", "description", "country")


@register(MovieShots)
class MovieShotsTranslationOptions(TranslationOptions):
    fields = ("title", "description")