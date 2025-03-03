from django.shortcuts import render

# Create your views here.

def index(request):
  return render(request, "app/index.html")

def profile(request):
  context_dict = {
    'user': {
      'name': "Example Name",
      'email': "example@domain.com",
      'username': "ExampleUserName",
      'rating': 4.7 
    }
  }
  return render(request, "app/profile.html", context=context_dict);

def register(request):
  return render(request, "app/register.html");

def login(request):
  return render(request, "app/login.html");