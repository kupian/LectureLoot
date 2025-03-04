from django.contrib import admin
from app.models import Category, Listing, CustomUser

class ListingAdmin(admin.ModelAdmin):
  list_display = ('title', 'category', 'id')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'name':('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(CustomUser)
