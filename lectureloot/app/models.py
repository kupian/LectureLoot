from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import datetime, timedelta

# User Model
class Bid():
    pass
class CustomUser(AbstractUser):
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

    def __str__(self):
        # return username when printing the user object
        return self.username
    
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
    highest_bid = models.OneToOneField("Bid", null=True, on_delete=models.SET_NULL, related_name="listing")
    # category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category", help_text="Category of item")
    # optional description of the item
    description = models.TextField(blank = True, null = True)
    # optional image for the listing; images will be uploaded to 'listing_images/'
    image = models.ImageField(
        upload_to = 'listing_images/',
        blank = True,
        null = True
    )

    # automatically set the time when the listing is created 
    created_at = models.DateTimeField(auto_now_add = True)
    
    one_week = datetime.now() + timedelta(weeks=1)
    end_datetime = models.DateTimeField(default=one_week)

    # automatically update the time whenever the listing is modified 
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        # display the listing title along with the sellers username for clarity
        return f"{self.title} (Seller: {self.seller.username})"
        
# define a new model to represent Bid
class Bid(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=False)
    amount = models.DecimalField(blank=False, decimal_places=2, max_digits=6)
    time = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"Bid on {self.listing} for £{self.amount}"
    