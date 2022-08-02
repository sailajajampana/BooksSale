from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from user_app.api.models import User
from books_app.api import models
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.authtoken.models import Token

# Create your tests here.

class BookListTestCase(APITestCase):
    def authentication(self):
        user=User.objects.create_user(username='username1',email='username1@gmail.com',password='password',
                                      contact_through='Email',city='Hyderabad')
        self.token,_=Token.objects.get_or_create(user_id=user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+str(self.token))
        
    
    def setUp(self):
        self.user=User.objects.create_user(username='username',email='username@gmail.com',password='password',
                                      contact_through='Email',city='Hyderabad')
        self.token,_=Token.objects.get_or_create(user_id=self.user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+str(self.token))
        self.genre=models.Genre.objects.create(name='Technology')
        
    def json_data(self,bookname):
        image=open('E:/drf-project/sellbooks_project/uploads/activity_2_vIb2E1x.PNG','rb')
        data={
            'picture':image,#SimpleUploadedFile(name="IMG-20201110-WA0007.jpg",content=b'',content_type="image/jpg"),
            'name':bookname,
            'cost':100,
            'genre': [self.genre.name],
 
        }
        return data
        
    def create_book(self):
        data=self.json_data('Django for beginners')
        response=self.client.post(reverse('books-list'),data,format='multipart')
        return response
         
    
    def test_book_create(self):
        response=self.create_book()
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(models.Book.objects.count(),1)
        self.assertEqual(response.data['cost'],100)
        
    def test_book_list(self):
        book=self.create_book()
        response=self.client.get(reverse('books-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(models.Book.objects.count(),1)
        
    def test_book_retreive(self):
        book=self.create_book()
        response=self.client.get(reverse('books-detail',args=(book.data['id'],)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['name'],'Django for beginners')
        
    def test_book_update(self):
        book=self.create_book()
        data=self.json_data('Django for professionals')
        response=self.client.put(reverse('books-detail',args=(book.data['id'],)),data,format='multipart')
        
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['name'],'Django for professionals')
    
    def test_book_update_not_seller(self):
        book=self.create_book()
        self.authentication()
        data=self.json_data('Django for professionals')
        response=self.client.put(reverse('books-detail',args=(book.data['id'],)),data,format='multipart')
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
    
    def test_book_delete(self):
        book=self.create_book()
        response=self.client.delete(reverse('books-detail',args=(book.data['id'],)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        
    def test_book_delete_not_seller(self):
        book=self.create_book()
        self.authentication()
        response=self.client.delete(reverse('books-detail',args=(book.data['id'],)))
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)
        
        
        

        
        
        
        
        
        
class GenreListTestCase(APITestCase):
    
    def setUp(self):
        self.user=User.objects.create_user(username='username',email='username@gmail.com',password='password',
                                        contact_through='Email',city='Hyderabad',is_staff=True)
        self.token,_=Token.objects.get_or_create(user_id=1)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+str(self.token))
        self.genre=models.Genre.objects.create(name='Technology')
        
    def test_genre_create(self):
        data={
            'name':'Thriller'
        }
        response=self.client.post(reverse('genre-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(models.Genre.objects.count(),2)
        
    def test_genre_list(self):
        response=self.client.get(reverse('genre-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(models.Genre.objects.count(),1)
    
    
        
        

        
        
        
        
        
    
        

    