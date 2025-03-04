import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lectureloot.settings')

import django
django.setup()
from app.models import Category, Listing, CustomUser

def populate():
    
    seller = CustomUser.objects.get_or_create(username = "johndoe", email="john@doe.com")[0]
    seller.save()
    seller_id = seller.pk

    stationery_pages = [
    {'title': 'Pencil', 'url': 'http://stationaryURL1/', 'price': 1.50, 'seller_id': seller_id},
    {'title': 'Highlighter', 'url': 'http://stationaryURL2/', 'price': 2.00, 'seller_id': seller_id}
    ]

    tech_pages = [
        {'title': 'Computer', 'url': 'http://www.techURL1/', 'price': 899.99, 'seller_id': seller_id},
        {'title': 'Headphones', 'url': 'http://www.techURL2/', 'price': 149.99, 'seller_id': seller_id}
    ]

    toys_pages = [
        {'title': 'Ball', 'url': 'http://toysURL1', 'price': 10.00, 'seller_id': seller_id},
        {'title': 'Play-Dough', 'url': 'http://toysURL2', 'price': 5.50, 'seller_id': seller_id}
    ]

    entertainment_pages = [
        {'title': 'Puzzle', 'url': 'http://entertainmentURL1', 'price': 15.99, 'seller_id': seller_id},
        {'title': 'Nintendo Switch', 'url': 'http://entertainmentURL2', 'price': 299.99, 'seller_id': seller_id}
    ]

    books_pages = [
        {'title': 'Harry Potter', 'url': 'http://booksURL1', 'price': 12.99, 'seller_id': seller_id},
        {'title': 'Java for Beginners', 'url': 'http://booksURL2', 'price': 29.99, 'seller_id': seller_id}
    ]

    food_pages = [
        {'title': 'Pasta Noodles', 'url': 'http://foodURL1', 'price': 3.99, 'seller_id': seller_id},
        {'title': 'Canned Beets', 'url': 'http://foodURL2', 'price': 2.49, 'seller_id': seller_id}
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
            add_listing(c, p['title'], p['url'], p['price'], p['seller_id'])
    
    for c in Category.objects.all():
        for p in Listing.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_listing(cat, title, url, price, seller_id, views=0):
    p = Listing.objects.get_or_create(category=cat, title=title, price=price, seller_id=seller_id)[0]
    p.url = url
    p.views=views
    p.price = price
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
    
    


    
