from django.contrib import admin
from .models  import (Category, 
                        Listing, 
                        User,
                        Bid,
                        Comment,
                        WatchList
                    )

# Register your models here.

class ListingAdmin(admin.ModelAdmin):
    list_display= (
        "winner",
        "title",
        
        "image",
        "status",
        "created_at",
    )
    list_filter= ["status"]

class BidAdmin(admin.ModelAdmin):
    list_display=(
        "bidder",
        "product",
        "price",
        "product_id"
    )

class CommentAdmin(admin.ModelAdmin):
    list_display=(
        "user",
        "subject",
    )
class WatchListAdmin(admin.ModelAdmin):
    list_display=(
        "id",
        "user",
        "watchlist",
        "watchlist_id"
    )

admin.site.register(Category)
admin.site.register(Listing,ListingAdmin)
admin.site.register(User)
admin.site.register(Bid,BidAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(WatchList, WatchListAdmin)