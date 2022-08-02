from django.db import models
from django.conf import settings
# Create your models here.
class Genre(models.Model):
    name=models.CharField(max_length=100,primary_key=True)
    def __str__(self):
        return self.name


class Book(models.Model):
    picture=models.ImageField(upload_to='uploads/')
    name=models.CharField(max_length=255,blank=False)
    seller=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='user_book')
    cost=models.PositiveIntegerField()
    genre=models.ManyToManyField(Genre,related_name='books')
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
