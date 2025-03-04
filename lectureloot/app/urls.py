from django.urls import path
from app import views
from django.contrib import admin

app_name = 'app'

urlpatterns = [
  # Home/Index view
  path('', views.index, name='index'),
  path('admin/', admin.site.urls),
  # Detail view for specific listing, using its pk
  path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
  # View to create a new listing; only accessible by logged-in users
  path('listing/new/', views.listing_create, name='listing_create'),
  path('search/<str:query>/', views.search, name="search"),
]
