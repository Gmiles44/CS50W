from django.contrib import admin

# Register your models here.
from .models import User, Listing, Bid

class ListingAdmin(admin.ModelAdmin):
    list_display = ("item_name", "starting_price")


admin.site.register(Listing, ListingAdmin)
admin.site.register(User)
admin.site.register(Bid)