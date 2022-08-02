from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from user_app.api.models import User


# Create your tests here.
class RegisterTestCase(APITestCase):
    def test_register(self):
        data={
            'username':'user',
            'email':'user1@gmail.com',
            'password':'password',
            'password2':'password',
            'phonenumber':'9876543210',
            'contact_through':'Phone',
            'city':'Chennai'
            
        }
        response=self.client.post(reverse('userapp:register'),data)
        self.assertEqual(response.data['email'],'user1@gmail.com')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
    def test_register_password_not_equal(self):
        data={
            'username':'user',
            'email':'user1@gmail.com',
            'password':'password',
            'password2':'password2',
            'phonenumber':'9876543210',
            'contact_through':'Phone',
            'city':'Chennai'
            
        }
        response=self.client.post(reverse('userapp:register'),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0],'passwords are different')
        
        
class LoginTestCase(APITestCase):
    def create_user(self):
        self.user=User.objects.create_user(username='username1',email='username1@gmail.com',password='password',
                                      contact_through='Email',city='Hyderabad')
        
    def test_login_success(self):
        self.create_user()
        data={
            'email':'username1@gmail.com',
            'password':'password'
        }
        response=self.client.post(reverse('userapp:login'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['Response'],'Login Successful')
        
    def test_login_unsuccessful(self):
        data={
            'email':'username1@gmail.com',
            'password':'password1'
        }
        response=self.client.post(reverse('userapp:login'),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'],'Login failed')
        
    def test_login_incomplete_request(self):
        data={
            'email':'username1@gmail.com'
        }
        response=self.client.post(reverse('userapp:login'),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['errors'],'Please provide both username and password')
        
class LogoutTestCase(APITestCase):
    def authentication(self):
        user=User.objects.create_user(username='username2',email='username2@gmail.com',password='password',
                                      contact_through='Email',city='bangalore')
        self.token,_=Token.objects.get_or_create(user_id=user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+str(self.token))
        
    def test_logout(self):
        self.authentication()
        response=self.client.post(reverse('userapp:logout'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['response'],'Logout successfully')
        
    def test_logout_without_login(self):
        response=self.client.post(reverse('userapp:logout'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['response'],'User is not logged in')
        
class PasswordChangeTestCase(APITestCase):
    def authentication(self):
        user=User.objects.create_user(username='username2',email='username2@gmail.com',password='password',
                                      contact_through='Email',city='bangalore')
        self.token,_=Token.objects.get_or_create(user_id=user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+str(self.token))
        return user
        
    def test_passwordchange(self):
        user=self.authentication()
        data={
           
            'password':'password1',
            'password2':'password1'
        }
        
        response=self.client.put(reverse('userapp:passwordchange'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['response'],'Password changed successfully')
        
    def test_passwordchange_not_authenticated(self):
        data={
           
            'password':'password1',
            'password2':'password1'
        }
        response=self.client.put(reverse('userapp:passwordchange'),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_passwordchange_password_mismatch(self):
        user=self.authentication()
        data={
           
            'password':'password1',
            'password2':'password2'
        }
        response=self.client.put(reverse('userapp:passwordchange'),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
class UserDetailsTestCase(APITestCase):
    
    def authentication(self,username,email):
        user=User.objects.create_user(username=username,email=email,password='password',
                                      contact_through='Email',city='Bangalore')
        self.token,_=Token.objects.get_or_create(user_id=user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token '+str(self.token))
        return user
    
    def test_userdetailschange(self):
        user=self.authentication('username2','user2@gmail.com')
        data={
            'username':'username2',
            'email':'user1@gmail.com',
            'phonenumber':'9876543210',
            'contact_through':'Phone',
            'city':'Bangalore'
            
        }
        
        response=self.client.put(reverse('userapp:update'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['response'],'User details updated successfully')
        
    def test_userdetailschange_not_authenticated(self):
        data={
            'username':'username2',
            'email':'user1@gmail.com',
            'phonenumber':'9876543210',
            'contact_through':'Phone',
            'city':'Bangalore'
            
        }
        
        response=self.client.put(reverse('userapp:update'),data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_userdetailsretrieve(self):
        user=self.authentication('username1','username1@gmail.com')
        user2=self.authentication('username2','username2@gmail.com')
        response=self.client.get(reverse('userapp:details',args=(1,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['city'],user.city)
        self.assertEqual(response.data['email'],user.email)
        
        
        
        
    
    
         
        
        

        
         
        
        
        
        
               
        
