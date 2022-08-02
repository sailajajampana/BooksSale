from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from books_app.api.models import Book, Genre
from books_app.api.permissions import IsAdminOrReadOnly, IsSellerOrReadOnly
from books_app.api.serializers import BookSerializer, GenreSerializer

class BookList(ListCreateAPIView):
    filter_backends=[DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filter_fields=['seller__city']
    search_fields=['name']
    ordering_fields=['modified_date','cost']
    parser_classes=(MultiPartParser,)
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    
    def perform_create(self,serializer):
        serializer.save(seller=self.request.user)
    
    
        
    
class BookDetail(RetrieveUpdateDestroyAPIView):
    parser_classes=(MultiPartParser,)
    queryset=Book.objects.all()
    serializer_class=BookSerializer
    permission_classes=[IsSellerOrReadOnly]
    
class GenreList(ListCreateAPIView):
    permission_classes=[IsAdminOrReadOnly]
    queryset=Genre.objects.prefetch_related('books')
    serializer_class=GenreSerializer
    

class GenreDetail(RetrieveUpdateDestroyAPIView):
    queryset=Genre.objects.prefetch_related('books')
    serializer_class=GenreSerializer
    lookup_field='name'
    permission_classes=[IsAdminOrReadOnly]
    
    



