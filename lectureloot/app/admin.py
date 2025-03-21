from django.contrib import admin
from app.models import Category, Listing, CustomUser, Media, Bid

class ListingAdmin(admin.ModelAdmin):
  list_display = ('title', 'category', 'id')

class CategoryAdmin(admin.ModelAdmin):
  prepopulated_fields = {'name':('name',)}

class MediaAdmin(admin.ModelAdmin):
  list_display = ('listing', 'file', 'media_type')

    

admin.site.register(Category, CategoryAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(CustomUser)
admin.site.register(Media, MediaAdmin)
admin.site.register(Bid)

