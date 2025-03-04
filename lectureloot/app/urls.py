from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
  path('', views.index, name='index'),
  path('profile/', views.profile, name='profile'),
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('profile/change-password/', views.change_password, name='change-password'),
  path('profile/edit/', views.edit_profile, name='edit_profile'),

]