from django.urls import path
from app import views
from django.contrib import admin

app_name = 'app'

urlpatterns = [
  # Home/Index view
  path('', views.index, name='index'),
  path('profile/', views.profile, name='profile'),
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('profile/change-password/', views.change_password, name='change-password'),
  path('profile/edit/', views.edit_profile, name='edit_profile'),
  path('admin/', admin.site.urls),
  # Detail view for specific listing, using its pk
  path('listing/<int:pk>/', views.listing_detail, name='listing_detail'),
  # View to create a new listing; only accessible by logged-in users
  path('listing/new/', views.listing_create, name='listing_create'),
  path('search/<str:query>/', views.search, name="search"),
  # URL pattern for the categories page
  path('categories/', views.categories, name='categories'),
  path('category/<str:name>/', views.category, name='category'),
  path('bid/<int:listing_id>', views.submit_bid, name="submit_bid"),
]