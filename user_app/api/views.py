from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from user_app.api.models import User
from user_app.api.serializers import (PasswordChangeSerializer,
                                      UserDetailSerializer,
                                      UserLoginSerializer,
                                      UserRegisterSerializer)

# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class=UserRegisterSerializer
    queryset=User.objects.all()
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
        
class LoginView(generics.GenericAPIView):
    serializer_class=UserLoginSerializer
    def post(self,request):
      
        email=request.POST.get('email')
        password=request.POST.get('password')
        if email and password:
            user=authenticate(request,email=email,password=password)
            if(user is not None):
                data={}
                data['Response']='Login Successful'
                token,_=Token.objects.get_or_create(user=user)
                data['token']=str(token)
                return Response(data)
            else:
                return Response({'errors':'Login failed'},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'errors':'Please provide both username and password'},status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(generics.RetrieveUpdateAPIView):
    permission_classes=[IsAuthenticated,]
    serializer_class=UserDetailSerializer
    queryset=User.objects.all()
    def put(self,request,pk=None):
                  
        user=User.objects.get(pk=request.user.pk)

        if(user is not None):
            serializer=self.serializer_class(user,data=request.data)
            if(serializer.is_valid(raise_exception=True)):
                serializer.save()
                return Response({'response':'User details updated successfully'})
            else:
                return Response(serializer.data)


class PasswordChangeView(generics.GenericAPIView):
    serializer_class=PasswordChangeSerializer
    queryset=User.objects.all()
    permission_classes=[IsAuthenticated,]
    def put(self,request,pk=None):    
        user=User.objects.get(pk=request.user.pk)

        if(user is not None):
            serializer=self.serializer_class(user,data=request.data)
            if(serializer.is_valid(raise_exception=True)):
                serializer.save()
                return Response({'response':'Password changed successfully'})
            else:
                return Response(serializer.data)
        
            
        
    
    
class LogoutView(APIView):
    def post(self,request):
        if request.user is not None and request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response({'response':'Logout successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'response':'User is not logged in'},status=status.HTTP_200_OK)
            
    
        
        
        
        
        