from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

STATUS=[
    ("active","active"),
    ("sold","sold"),
    ("deleted","deleted")

]


class User(AbstractUser):
    pass

class Category(models.Model):
    name=models.CharField(max_length=40)
    
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    user=models.ForeignKey(User, related_name="user",on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    image=models.URLField(max_length=1000,blank=True)
    starting_price=models.FloatField(default=0)
    category=models.ForeignKey(Category,related_name="category", on_delete=models.CASCADE)
    status=models.CharField(
        max_length=7,
        choices=STATUS,
        default="active"
    )
    created_at=models.DateTimeField(default=datetime.now())
    winner=models.ForeignKey(User,related_name="winner",blank=True, null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    subject=models.CharField(max_length=50)
    entry=models.TextField()
    user=models.ForeignKey(User,related_name="c_user",on_delete=models.CASCADE)
    item=models.ForeignKey(Listing,related_name="item", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject}"

class Bid(models.Model):
    bidder=models.ForeignKey(User, related_name="bidder",on_delete=models.CASCADE)
    price=models.FloatField(default=0)
    product=models.ForeignKey(Listing, related_name="product", on_delete=models.CASCADE)
    date=models.DateTimeField(default=datetime.now())
    
    def __str__(self):
        return f"{self.product}"

class WatchList(models.Model):
    
    user=models.ForeignKey(User,related_name="watchlist_user", on_delete=models.CASCADE)
    watchlist=models.ForeignKey(Listing, related_name="watchlist", blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} added {self.watchlist} to watchlist"