# LectureLoot

# How to run

We recommend using Python 3.11 and Django 2.2.28

`pip install -r requirements.txt`
`python manage.py makemigrations app` (may need to run this multiple times)
`python manage.py migrate`
`python populate_app.py` to fill the database with test data
`python manage.py runserver` to begin running the debug server
`python manage.py periodic_listing_check` in a separate terminal to begin running the listing end service