import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lectureloot.settings')

import django
django.setup()
from app.models import Category, Page

def populate():

    stationary_pages = [
        {'title': 'Pencil',
         'url': 'http://stationaryURL1/'},
         {'title':'Highlighter',
          'url': 'http://stationaryURL2/'} ]
    
    tech_pages = [        
        {'title': 'Computer',
         'url': 'http://www.techURL1/'},
         {'title':'Headphones',
          'url': 'http://www.techURL2/'} ]

    toys_pages = [
        {'title': 'Ball',
         'url': 'http://toysURL1'},
         {'title':'Play-Dough',
          'url': 'http://toysURL2'} ]
    
    entertainment_pages = [
        {'title': 'Puzzle',
         'url': 'http://entertainmentURL1'},
         {'title':'Nintendo Switch',
          'url': 'http://entertainmentURL1'} ]
    
    books_pages = [
        {'title': 'Harry Potter',
        'url': 'http://booksURL1'},
         {'title':'Java for Beginners',
          'url': 'http://booksURL2'} ]
    
    food_pages = [
       {'title': 'Pasta Noodles',
         'url': 'http://foodURL1'},
         {'title':'Canned Beets',
          'url': 'http://foodURL2'} ]
    
    cats = {'Stationary': {'pages': stationary_pages},
             'Tech': {'pages': tech_pages},
             'Toys': {'pages': toys_pages}, 
             'Entertainment': {'pages': entertainment_pages} }
             'Books': {'pages': books_pages},
             'Food': {'pages': food_pages} }
    
    for cat, cat_data in cats.items():
        c = add_category(cat)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])
    
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views=views
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
    
    


    
