from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if email is None:
            raise TypeError("Usere should have email")
        email=self.normalize_email(email)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password=None,**extra_fields):
        if password is None:
            raise TypeError("password should not be none")
        user=self.create_user(email,password,**extra_fields)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    CONTACT_CHOICES=(
        ('Phone','Phonenumber'),
        ('Email','Email'),
    )
    username=models.CharField(max_length=225,unique=True)
    email=models.EmailField(max_length=255,unique=True)
    phonenumber=models.CharField(blank=True,max_length=10)
    city=models.CharField(max_length=255,null=True)
    contact_through=models.CharField(max_length=5,choices=CONTACT_CHOICES)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    objects=UserManager()
    
    def __str__(self):
        return self.email 
    
    
    


    