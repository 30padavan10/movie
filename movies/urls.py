from django.urls import path

from . import views

urlpatterns = [
    path('', views.MovieView.as_view()),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name='movie_detail'),
    path('add-rating/', views.AddStarRating.as_view(), name='add_rating')
]