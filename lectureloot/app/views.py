from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse
from django.utils.timezone import now
from .models import Listing, Category, Bid, CustomUser, Media
from .forms import ListingForm, MediaForm MediaFormSet

# Listing view
def listing_detail(request, pk):
  """
  Retrieve and display details for a single listing
  'pk' is the primary key for a given listing
  """
  # retrieve the listing; if not found, return a 404 error
  listing = get_object_or_404(Listing, pk = pk)

  media = Media.objects.filter(listing=listing)

  # render the 'listing_detail.html' template with the listing context
  return render(request, 'app/listing_details.html', {'listing':listing,'media':media})

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
    files = [file for key, file in request.FILES.items() if key.startswith('form-') and key.endswith('-file')]
    print(files)

    if form.is_valid():
      # create a new listing instance without saving to the database
      new_listing = form.save(commit = False)
      # set the seller to the currently logged in user
      new_listing.seller = request.user
      # save the listing to the database
      new_listing.save()

      # Save media files associated with the listing
      for file in files:       
        media_type = 'video' if file.content_type.startswith('video') else 'image'
        Media.objects.create(listing=new_listing, file=file, media_type=media_type)

      # redirect to the detail view for the newly created listing
      return redirect('app:listing_detail', pk = new_listing.pk)
  else:
    # if GET request, create an empty form
    form = ListingForm()
    MediaFormSet = modelformset_factory(Media, form=MediaForm, extra=1, max_num=10, can_delete=True)
    media_formset = MediaFormSet(queryset=Media.objects.none())

  # render the 'listing_create.html' template with the form context
  return render(request, 'app/listing_create.html', {'form':form,'media_formset':media_formset})

# index view
def index(request):
  return render(request, "app/index.html")

# profile view
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

# register view
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

# edit profile view
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

# login view
def login(request):
  return render(request, "app/login.html")

# change password view
def change_password(request):
  return render(request, "app/change_password.html")

# search view
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

# categories list
def categories(request):
  '''Retrieve all Category objects from the database and render the categories page'''

  # Query all Category instances
  all_categories = Category.objects.all()

  # prepare the context to pass into template
  context = {
    'categories': all_categories,
  }

  # render the 'categories.html' template within the 'app' folder
  return render(request, 'app/categories.html', context=context)

# category view
def category(request, name):
  category = Category.objects.get(name=name)
  if category is None:
    listings = None
  else:
    listings = Listing.objects.filter(category = category)
    
  context = {
    "name": name,
    "listings": listings,
  }
  return render(request, 'app/category.html', context=context)

def submit_bid(request, listing_id):
  if request.user.is_authenticated is False:
    return JsonResponse({
      "message": "You must be logged in to place a bid",
    }, status=403)
  
  listing = Listing.objects.get(pk=listing_id)
  amount = float(request.POST.get("amount", 0))
  if listing is None:
    return JsonResponse({
    "message": "Invalid listing"
    }, status=403)
    
  if listing.end_datetime < now():
    return JsonResponse({
      "message": "Listing has ended"
    }, status=403)
  
  try:
    highest_bid_amount = listing.highest_bid.amount
  except AttributeError:
    highest_bid_amount = 0

  if amount <= highest_bid_amount:
    return JsonResponse({
      "message": "Amount must be greater than highest bid"
    }, status=403)
    
  bid = Bid(listing=listing, user=request.user, amount=amount)
  bid.save()
  
  listing.highest_bid = bid
  listing.save()
  
  return JsonResponse({
    "message": "success"
  })

def merchant(request, username):
  media_path = settings.MEDIA_URL

  if username: 
    user = get_object_or_404(CustomUser, username=username)
    
    context = {
      "user": user
    }

  return render(request, "app/merchant.html", context)
