import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lectureloot.settings')
import django
django.setup()
from app.models import Category, Listing, CustomUser, Bid, Media
from django.core.files import File
from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
import pathlib

def populate():
    # create or get the seller
    seller = CustomUser.objects.get_or_create(username = "johndoe", email="john@doe.com")[0]
    seller.save()
    seller_id = seller.pk
    # update data dictionaries with the new "description" field.
    stationery_pages = [
    {'title': 'Pencil', 'url': 'http://stationaryURL1/', 'seller_id': seller_id, 'description': 'A high-quality pencil', 'image':f'pencil.jpg'},
    {'title': 'Highlighter', 'url': 'http://stationaryURL2/', 'seller_id': seller_id, 'description': 'Bright highlighter for notes', 'image':f'highlighter.jpg'}
    ]

    tech_pages = [
        {'title': 'Computer', 'url': 'http://www.techURL1/', 'seller_id': seller_id, 'description': 'Powerful desktop computer', 'image':f'computer.jpg'},
        {'title': 'Headphones', 'url': 'http://www.techURL2/', 'seller_id': seller_id, 'description': 'Noise-cancelling headphones', 'image':f'headphones.jpg'}
    ]

    toys_pages = [
        {'title': 'Ball', 'url': 'http://toysURL1', 'seller_id': seller_id, 'description': 'Bouncy ball for play', 'image':f'ball.jpg'},
        {'title': 'Play-Dough', 'url': 'http://toysURL2', 'seller_id': seller_id, 'description': 'Colorful play-dough', 'image':f'playdough.jpg'}
    ]

    entertainment_pages = [
        {'title': 'Puzzle', 'url': 'http://entertainmentURL1', 'seller_id': seller_id, 'description': 'Challenging jigsaw puzzle', 'image':f'puzzle.jpg'},
        {'title': 'Nintendo Switch', 'url': 'http://entertainmentURL2', 'seller_id': seller_id, 'description': 'Popular gaming console', 'image':f'nintendo.jpg'}
    ]

    books_pages = [
        {'title': 'Harry Potter', 'url': 'http://booksURL1', 'seller_id': seller_id, 'description': 'Fantasy novel series', 'image':f'book1.jpg'},
        {'title': 'Java for Beginners', 'url': 'http://booksURL2', 'seller_id': seller_id,'description': 'Introductory programming book', 'image':f'book2.jpg'}
    ]

    food_pages = [
        {'title': 'Pasta Noodles', 'url': 'http://foodURL1', 'seller_id': seller_id, 'description': 'Delicious pasta noodles', 'image':f'pasta.jpg'},
        {'title': 'Canned Beets', 'url': 'http://foodURL2', 'seller_id': seller_id, 'description': 'Healthy canned beets', 'image':f'beets.jpg'}
    ]
    
    cats = {'Stationery': {'pages': stationery_pages},
             'Tech': {'pages': tech_pages},
             'Toys': {'pages': toys_pages}, 
             'Entertainment': {'pages': entertainment_pages},
             'Books': {'pages': books_pages},
             'Food': {'pages': food_pages} }
    
    # define a mapping for dummy bid prices
    price_mapping = {
        'Stationery':5,
        'Tech': 250,
        'Toys': 10,
        'Entertainment':50,
        'Books':15,
        'Food':8,
    }
    
    for cat, cat_data in cats.items():
        c = add_category(cat)
        for p in cat_data['pages']:
            image_path = p.get('image')
            # assign the return value of add_listing to variable 'listing'
            listing = add_listing(c, p['title'], p['url'], p['seller_id'], description=p.get('description', ''), image_path=image_path)
            # create a dummy bid using the mapping or a default value
            bid_price = price_mapping.get(cat, 10)
            add_dummy_bid(listing, bid_price)
    # output the created categories, listings, and bids for verification
    for c in Category.objects.all():
        for listing in Listing.objects.filter(category=c):
            print(f'- {c}: {listing}')
            for bid in Bid.objects.filter(listing=listing):
                print(f'    - Dummy Bid by {bid.user}: £{bid.amount}')

def add_listing(cat, title, url, seller_id, views=0, description="", image_path=None):
    # retrieve/create the Listing instance.
    listing = Listing.objects.get_or_create(category=cat, title=title, seller_id=seller_id)[0]
    listing.url = url
    listing.views=views
    listing.description = description # new field added
    listing.seller = CustomUser.objects.get(pk=seller_id)
    # attach media file if image_path is provided
    if image_path:
        # construct the full path to the media file.
        safe_filename = pathlib.Path(image_path).name
        full_path = f"media/example_images/{safe_filename}"
        
        if os.path.exists(full_path):
            with open(full_path, 'rb') as f:
                file = File(f)
                media = Media(listing=listing, file=file, media_type="image")
                media.save()
        else:
            print(f"Image file not found: {full_path}")
    listing.save()
    return listing

def add_category(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

def add_dummy_bid(listing, price):
    # create a dummy bid for the listing with the provided price. 
    # currently using: listing seller -- can be adjusted if needed.
    dummy_bid = Bid.objects.get_or_create(listing=listing, user=listing.seller, amount=price)[0]
    dummy_bid.save()
    listing.highest_bid = dummy_bid
    listing.save()
    return dummy_bid

# Start execution
if __name__ == '__main__':
    print('Starting App population script...')
    populate()