from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Listing
from .forms import ListingForm 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages

# Listing views
def listing_detail(request, pk):
  """
  Retrieve and display details for a single listing
  'pk' is the primary key for a given listing
  """
  # retrieve the listing; if not found, return a 404 error
  listing = get_object_or_404(Listing, pk = pk)
  # render the 'listing_detail.html' template with the listing context
  return render(request, 'app/listing_details.html', {'listing':listing})

@login_required
def listing_create(request):
  '''
  Handle the creation of a new listing.
  - GET: display an empty form.
  - POST: validate and save the form data.
  '''
  if request.method == 'POST':
    # create a form instance with the POST data and uploaded files
    form = ListingForm(request.POST, request.FILES)
    if form.is_valid():
      # create a new listing instance without saving to the database
      new_listing = form.save(commit = False)
      # set the seller to the currently logged in user
      new_listing.seller = request.user
      # save the listing to the database
      new_listing.save()
      # redirect to the detail view for the newly created listing
      return redirect('app:listing_detail', pk = new_listing.pk)
  else:
    # if GET request, create an empty form
    form = ListingForm()
  # render the 'listing_create.html' template with the form context
  return render(request, 'app/listing_create.html', {'form':form})

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
  if request.method == "POST":
    email = request.POST.get("email")
    password = request.POST.get("password1")
    user = authenticate(request, username=email, password=password)
    if user:
      if user.is_active:
        auth_login(request, user)
        return redirect("app:index")
      else:
        messages.error(request, "User is not active")
    else:
      messages.error(request, "Invalid login details") 
  else:
      
    return render(request, "app/login.html")

def change_password(request):
  return render(request, "app/change_password.html")

def search(request, query):
  media_path = settings.MEDIA_URL
  
  if query:
    query_matches = Listing.objects.filter(title__icontains=query)
    
    context = {
      "query": query,
      "results": query_matches,
    }
    
    print(query_matches)
  
  return render(request, "app/search.html", context)

def logout(request):
  auth_logout(request)
  return redirect("app:index")
  
