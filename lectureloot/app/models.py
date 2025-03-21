from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime, timedelta

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # decimal field to store the user rating (e.g., 0.00 to 5.00)
    rating = models.DecimalField(
        max_digits = 3, # max number of digits 
        decimal_places = 2, # number of decimal places
        default = 0.00, # default rating value
        help_text = "User's overall ratiing"
    )

    # optional profile picture for the user; images will be uploaded to 'profile_pictures/'
    profile_project = models.ImageField(
        upload_to = 'profile_pictures/',
        blank = True, # field is optional
        null = True # field can be null in the database 
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    def __str__(self):
        return self.email
    
class Category(models.Model):
    MAX_NAME_LENGTH = 128
    name = models.CharField(max_length=MAX_NAME_LENGTH, unique=True)
    description = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

# Listing Model
class Listing(models.Model):
    # link the listing to a seller (CustomUser) using a foreign key
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, # reference the custom user model
        on_delete = models.CASCADE, # delete listings if the seller is deleted
        related_name = 'listings', # allows reverse lookup: user.listings.all()
        help_text = "User who is selling this item."
    )

    # title of the listing
    title = models.CharField(max_length = 255)
    # price of the item, stored as a decimal number
    highest_bid = models.OneToOneField("Bid", null=True, on_delete=models.SET_NULL, related_name="winning_listing")
    # category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", help_text="Category of item")
    # optional description of the item
    description = models.TextField(blank = True, null = True)

    # automatically set the time when the listing is created 
    created_at = models.DateTimeField(auto_now_add = True)
    
    one_week = datetime.now() + timedelta(weeks=1)
    end_datetime = models.DateTimeField(default=one_week)

    # automatically update the time whenever the listing is modified 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        # display the listing title along with the sellers username for clarity
        return f"{self.title} (Seller: {self.seller.username})"
    
# Many to one media (includes image and video)
class Media(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='media')

    file = models.FileField(upload_to='listing_media/')
    
    media_type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])

    # code that automatically detects file type and saves it
    def save(self, *args, **kwargs):
        if self.file:
            if self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                self.media_type = 'image'
            elif self.file.name.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                self.media_type = 'video'
            else:
                raise ValueError('Unsupported file format')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Media for {self.listing.title} ({self.media_type})"
      
class Bid(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(blank=False, decimal_places=2, max_digits=6)
    time = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"Bid for £{self.amount}"
    