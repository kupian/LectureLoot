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
  return render(request, "app/profile.html", context=context_dict)

def register(request):
  context_dict = {
    'register': True,
    'values': {
      'firstName': "",
      'familyName': "",
      'email': "",
      'username': "",
    }
  }
  
  return render(request, "app/register.html", context=context_dict)

def edit_profile(request):
  context_dict = {
    'register': False,
    'values': {
      'firstName': "Example",
      'familyName': "Name",
      'email': "example@domain.com",
      'username': "ExampleUserName",
    }
  }

  return render(request, "app/register.html", context=context_dict)


def login(request):
  return render(request, "app/login.html")

def change_password(request):
  return render(request, "app/change_password.html")