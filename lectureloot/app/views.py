from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Listing, CustomUser, Category, Bid, Media, Notification
from .forms import ListingForm, UserForm, UserProfileForm, MediaForm, MediaFormSet 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils.timezone import now
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
 
# sort query matches by a query
def sort(query_matches, sort_by):
  if sort_by == "title":
    query_matches = query_matches.order_by("title")
  elif sort_by == "price_low":
    query_matches = query_matches.order_by("highest_bid__amount")
  elif sort_by == 'price_high':
    query_matches = query_matches.order_by('-highest_bid__amount')
  elif sort_by == 'end_datetime':
    query_matches = query_matches.order_by('end_datetime')
  return query_matches

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
      
      dummy_bid = Bid(user=request.user, amount=request.POST["price"], listing=new_listing)
      dummy_bid.save()
      
      new_listing.highest_bid = dummy_bid
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
    # get top 10 listings ending soon
    ending_soon = Listing.objects.filter(end_datetime__gt=now()).order_by('end_datetime')[:10]

    # get listings by category
    categories = Category.objects.all()
    category_listings = {category: Listing.objects.filter(category=category)[:5] for category in categories}

    context = {
        "ending_soon": ending_soon,
        "category_listings": category_listings
    }
    return render(request, "app/index.html", context)

# profile view
@login_required
def profile(request):
  form = UserProfileForm()
  if request.method == "POST":
    form = UserProfileForm(request.POST, request.FILES)
    if form.is_valid():
      user_profile = form.save(commit=False)
      user_profile.user = request.user
      user_profile.save()
      print(user_profile)
      return redirect('app:index')
    else:
      print(form.errors)
  user_listings = Listing.objects.filter(seller=request.user)
  context_dict = {'form': form, 'listings': user_listings}
  return render(request, "app/profile.html", context_dict)

def about(request):
  return render(request, 'app/about.html')

# search view
def search(request, query):
  media_path = settings.MEDIA_URL
  
  if query:
    query_matches = Listing.objects.filter(title__icontains=query)
    
    # handle sorting
    sort_by = request.GET.get("sort_by", "end_datetime")
    query_matches = sort(query_matches, sort_by)
    
    context = {
      "query": query,
      "results": query_matches,
      "sort_by": sort_by
    }
    
    print(query_matches)
  
  return render(request, "app/search.html", context)

@login_required
def logout(request):
  auth_logout(request)
  return redirect("app:index")
  
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
    
    sort_by = request.GET.get("sort_by", "end_datetime")
    listings = sort(listings, sort_by)
    
  context = {
    "name": name,
    "listings": listings,
    "sort_by": sort_by
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
    user_listings = Listing.objects.filter(seller=user)
    
    context = {
      "user": user,
      "listings": user_listings
    }

  return render(request, "app/merchant.html", context)

def highest_bid(request, listing_id):
  listing = Listing.objects.get(pk=listing_id)
  if listing is None:
    return JsonResponse({
    "message": "Invalid listing"
    }, status=403)
    
  amount = listing.highest_bid.amount
  user_id = listing.highest_bid.user.id
  
  context_dict = {
    "amount": amount,
    "user_id": user_id
  }
  
  return JsonResponse(context_dict)

@login_required
def notifications(request):
    """display user notifications and mark as read"""
    
    user_notifications = Notification.objects.filter(user=request.user)
    
    # mark as read
    unread_notifications = user_notifications.filter(read=False)
    unread_notifications.update(read=True)
    
    return render(request, 'app/notifications.html', {
        'notifications': user_notifications
    })
    
@login_required
def clear_notifications(request):
  """remove all notifications"""
  user_notifications = Notification.objects.filter(user=request.user)
  user_notifications.delete()
  return render(request, 'app/notifications.html', {
        'notifications': user_notifications
    })
 
# register view
def register(request):
  if request.method == "POST":
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")
 
    # Password validation
    if password1 != password2:
      messages.error(request, "Passwords do not match")
      return redirect("app:register")
 
    # Check if username/email already exists
    if CustomUser.objects.filter(email=email).exists():
      messages.error(request, "Email already in use")
      return redirect("app:register")
 
    if CustomUser.objects.filter(username=username).exists():
      messages.error(request, "Username already already in use")
      return redirect("app:register")
      
    # Create and save user
    user = CustomUser.objects.create_user(
      first_name=first_name,
      last_name=last_name,
      username=username,
      email=email,
      password=password1
    )
    auth_login(request, user)
    return redirect("app:index")
 
  return render(request, "app/register.html", {"register": True})
 
@login_required
# edit profile view
def edit_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return redirect("app:profile")
        else:
          messages.error(request, "SOmething already in use")
    else:
        form = UserForm(instance=user)
    return render(request, "app/register.html", {"form": form, "register": False})
 
# login view
def login(request):
  if request.method == 'POST':
    email = request.POST.get("email")
    password = request.POST.get('password1')
    user = authenticate(request, username=email, password=password)
    if user:
      if user.is_active:
        auth_login(request, user)
        return redirect("app:index")
      else:
        messages.error(request, "User is not active")
    else:
      messages.error(request, "Invalid login details")     
  return render(request, "app/login.html")
 
# change password view
def change_password(request):
  if request.method == "POST":
    current_password = request.POST.get('password')
    new_password = request.POST.get('password1')
    confirm_password = request.POST.get('password2')
    user = request.user
    if user.check_password(current_password):
      if new_password == confirm_password:
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return redirect('app:profile')
      else:
        messages.error(request, "New passwords do not match")
    else:
      messages.error(request, "Incorrect current password")
 
  return render(request, "app/change_password.html")