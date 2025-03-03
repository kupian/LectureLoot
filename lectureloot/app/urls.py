from django.urls import path
from app import views
from django.contrib import admin

app_name = 'app'

urlpatterns = [
  path('', views.index, name='index'),
  path('admin/', admin.site.urls),
]
