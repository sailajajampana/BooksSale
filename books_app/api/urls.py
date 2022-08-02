from django.urls import path, include
from books_app.api import views


urlpatterns = [
    path('books/',views.BookList.as_view(),name='books-list'),
    path('books/<int:pk>/',views.BookDetail.as_view(),name='books-detail'),
    path('genre/<str:name>/',views.GenreDetail.as_view(),name='genre-detail'),
    path('genre/',views.GenreList.as_view(),name='genre-list'),
    
]
