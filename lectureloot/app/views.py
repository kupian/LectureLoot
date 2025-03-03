from django.shortcuts import render
from django.conf import settings

# Create your views here.

def index(request):
  return render(request, "app/index.html")

def search(request, query):
  img_name = "pencil.jpg"
  media_path = settings.MEDIA_URL
  
  test_context = {
    "query": query,
    "results": [
      {
        "title": "Big pencil",
        "image_url": media_path + img_name,
        "price": 5000
      },
      {
        "title": "Other pencil",
        "image_url": media_path + img_name,
        "price": 2300
      },
      {
        "title": "Pen von cil",
        "image_url": media_path + img_name,
        "price": 7.56
      },
      {
        "title": "Pencil the fourth",
        "image_url": media_path + img_name,
        "price": 234927
      },
    ]
  }
  
  return render(request, "app/search.html", test_context)