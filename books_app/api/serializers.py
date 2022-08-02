from books_app.api.models import Book, Genre
from rest_framework import serializers
from rest_framework import status

class BookSerializer(serializers.ModelSerializer):
    genre=serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(),many=True)
    seller=serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model=Book
        fields=["id","genre","name","cost","seller","picture"]
        extra_kwargs={
            'seller':{'read_only':True}
        }
  
        
class GenreSerializer(serializers.ModelSerializer):
    books=BookSerializer(many=True,read_only=True)
    class Meta:
        model=Genre
        fields="__all__"
