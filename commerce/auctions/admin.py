from django.contrib import admin

# Register your models here.
from .models import User, Listing, Bid, Comment

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "item_name", "starting_price")


admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)