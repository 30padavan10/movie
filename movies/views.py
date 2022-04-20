from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .forms import RatingForm, ReviewForm

from .models import Movie, Rating, Category, Actor, Genre


class GenreYears:
    """Жанры и года выхода фильмов как альтернатива методу get_context_data"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")  # берем не все поля экземпляра, а только поле year
    # если использовать values("year") - выводится словать {'year': 1989}
    # в шаблоне обращаемся не напрямую к year, а как <переменная в for>.year
    # если использовать values_list("year") - выводится кортеж (1989,)

# class MovieView(View):
#     """Список фильмов"""
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, 'movies/movies.html', {'movie_list': movies})

class MovieView(GenreYears, ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'
    # context ListView будет состоять из {
    # 'paginator': None,
    # 'page_obj': None,
    # 'is_paginated': False,
    # 'object_list': <QuerySet [<Movie: Терминатор 2>, <Movie: Терминатор>]>,
    # 'movie_list': <QuerySet [<Movie: Терминатор 2>, <Movie: Терминатор>]>,
    #  'view': <movies.views.MovieView object at 0x0000025DABB5B910>
    #  }
    # при добавлении наследования GenreYears можно вызывать методы этого класса в шаблоне через параметр 'view'

    # def get_context_data(self, *args, **kwargs):            # чтобы выводить категории на каждой странице потребуется
    #     context = super().get_context_data(*args, **kwargs) # дублировать данный метод на каждую страницу, обойти
    #     context["categories"] = Category.objects.all()      # это можно либо созданием миксина или использовать
    #     return context                                      # simple_tag, будет показан пример с simple_tag


    
# class MovieDetailView(View):
#     """Подробная информация"""
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, 'movies/movie_detail.html', {'movie': movie})


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_details.html'
    slug_field = "url" # если бы поле модели назыв. slug, то переопределять не нужно, также и с pk эта строка не нужна

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context DetailView состоит из {
        # 'object': <Movie: Терминатор 2>,
        # 'movie': <Movie: Терминатор 2>,
        # 'view': <movies.views.MovieDetailView object at 0x000001EE2C664880>
        # }
        context['star_form'] = RatingForm()
        return context


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        #print(request.POST)
        form = ReviewForm(request.POST)
        if form.is_valid():
            # тут form это еще html текст. При вызове метода save создается объект формы
            form = form.save(commit=False)  # чтобы форма сразу не сохранялась нужен параметр commit=False
            # теперь form это объект и с ней можно работать
            # form.movie_id = pk  # в бд поле которое хранит значение связанной модели называется movie_id поэтому
            # можно обращаться напрямую к нему
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            movie = Movie.objects.get(pk=pk)
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())



class AddStarRating(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id = int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class ActorView(GenreYears, DetailView):
    """Информация об актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMovieView(GenreYears, ListView):
    """Фильтр фильмов"""
    template_name = "movies/movies.html"

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        )
        return queryset


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")  # distinct исключает повторение
        return queryset

    def get(self, request, *args, **kwargs):  # при вызове метода get
        queryset = list(self.get_queryset())    # вызываем метод get_queryset и оборачиваем в список
        return JsonResponse({"movies": queryset}, safe=False)  # с помощью JsonResponse передаем этот список





