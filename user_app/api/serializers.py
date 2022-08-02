from django.contrib.auth import get_user_model
from rest_framework import serializers

from user_app.api.models import User
from books_app.api.serializers import BookSerializer


def passwordlength_validator(value):
    if(len(value)<5):
        raise serializers.ValidationError('Password length should be greater than 5')

class UserRegisterSerializer(serializers.ModelSerializer):
    books=BookSerializer(many=True,required=False,read_only=True)
    password2=serializers.CharField(style={
        'input_type':'password'
    },
    write_only=True)
    password=serializers.CharField(style={
        'input_type' : 'password'
    }, write_only=True, validators=[passwordlength_validator,])
    class Meta:
        model=get_user_model()
        fields=['id','username','email','password','phonenumber','contact_through','password2','books','city']
        
    
    def save(self):
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if(password!=password2):
            raise serializers.ValidationError('passwords are different')
        self.validated_data.pop('password2')
        user=User.objects.create_user(**self.validated_data)
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={
        'input_type':'password'
    }, write_only=True)
    class Meta:
        model=get_user_model() 
        fields=["email","password"] 
        

class UserDetailSerializer(serializers.ModelSerializer):
    books=BookSerializer(many=True,required=False,read_only=True)
    email=serializers.EmailField(read_only=True)
    class Meta:
        model=get_user_model()
        fields=["username","email","phonenumber","contact_through","city","books"]
        
class PasswordChangeSerializer(serializers.ModelSerializer):
    
    password2=serializers.CharField(style={
        'input_type':'password'
    },
    write_only=True)
    password=serializers.CharField(style={
        'input_type' : 'password'
    }, write_only=True,validators=[passwordlength_validator,])
    
    class Meta:
        model=get_user_model()
        fields=['password','password2']
                
    def validate(self,data):
        if(data['password']!=data['password2']):
            raise serializers.ValidationError('passwords didnot match')
        return data
    
    
        
        
    
        
        
    
        
    
            
        
            
    

        
        
        
    

        
        