from django.urls import path, include
from user_app.api import views

app_name='userapp'
urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('update/',views.UserDetailView.as_view(),name='update'),
    path('<int:pk>/details/',views.UserDetailView.as_view(),name='details'),
    path('password_change/',views.PasswordChangeView.as_view(),name='passwordchange'),
    
    
]
