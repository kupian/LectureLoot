from django.urls import path
from app import views

app_name = 'app'

urlpatterns = [
  path('', views.index, name='index'),
  path('search/<str:query>/', views.search, name="search")
]