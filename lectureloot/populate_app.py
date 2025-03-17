import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lectureloot.settings')

import django
django.setup()
from app.models import Category, Listing, CustomUser

def populate():
    # create or get the seller
    seller = CustomUser.objects.get_or_create(username = "johndoe", email="john@doe.com")[0]
    seller.save()
    seller_id = seller.pk
    # update data dictionaries with the new "description" field.
    stationery_pages = [
    {'title': 'Pencil', 'url': 'http://stationaryURL1/', 'seller_id': seller_id, 'description': 'A high-quality pencil'},
    {'title': 'Highlighter', 'url': 'http://stationaryURL2/', 'seller_id': seller_id, 'description': 'Bright highlighter for notes'}
    ]

    tech_pages = [
        {'title': 'Computer', 'url': 'http://www.techURL1/', 'seller_id': seller_id, 'description': 'Powerful desktop computer'},
        {'title': 'Headphones', 'url': 'http://www.techURL2/', 'seller_id': seller_id, 'description': 'Noise-cancelling headphones'}
    ]

    toys_pages = [
        {'title': 'Ball', 'url': 'http://toysURL1', 'seller_id': seller_id, 'description': 'Bouncy ball for play'},
        {'title': 'Play-Dough', 'url': 'http://toysURL2', 'seller_id': seller_id, 'description': 'Colorful play-dough'}
    ]

    entertainment_pages = [
        {'title': 'Puzzle', 'url': 'http://entertainmentURL1', 'seller_id': seller_id, 'description': 'Challenging jigsaw puzzle'},
        {'title': 'Nintendo Switch', 'url': 'http://entertainmentURL2', 'seller_id': seller_id, 'description': 'Popular gaming console'}
    ]

    books_pages = [
        {'title': 'Harry Potter', 'url': 'http://booksURL1', 'seller_id': seller_id, 'description': 'Fantasy novel series'},
        {'title': 'Java for Beginners', 'url': 'http://booksURL2', 'seller_id': seller_id,'description': 'Introductory programming book' }
    ]

    food_pages = [
        {'title': 'Pasta Noodles', 'url': 'http://foodURL1', 'seller_id': seller_id, 'description': 'Delicious pasta noodles'},
        {'title': 'Canned Beets', 'url': 'http://foodURL2', 'seller_id': seller_id, 'description': 'Healthy canned beets'}
    ]
    
    cats = {'Stationery': {'pages': stationery_pages},
             'Tech': {'pages': tech_pages},
             'Toys': {'pages': toys_pages}, 
             'Entertainment': {'pages': entertainment_pages},
             'Books': {'pages': books_pages},
             'Food': {'pages': food_pages} }
    
    for cat, cat_data in cats.items():
        c = add_category(cat)
        for p in cat_data['pages']:
            add_listing(c, p['title'], p['url'], p['seller_id'], description=p.get('description', ''))
    
    for c in Category.objects.all():
        for p in Listing.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_listing(cat, title, url, seller_id, views=0, description=""):
    # retrieve or create the Listing instance.
    p = Listing.objects.get_or_create(category=cat, title=title, seller_id=seller_id)[0]
    p.url = url
    p.views=views
    p.description = description # new field added
    p.seller = CustomUser.objects.get(pk=seller_id)
    p.save()
    return p

def add_category(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

# Start execution
if __name__ == '__main__':
    print('Starting App population script...')
    populate()
    
    


    
