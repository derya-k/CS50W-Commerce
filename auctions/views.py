from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory

from .models import (User, 
                    Listing, 
                    Comment,
                    Category,
                    WatchList,
                    Bid
                    )
from .forms import (ListingForm, 
                    CommentForm,
                    BidForm,
                    )

def index(request):
    listings=Listing.objects.filter(status="active")
    
    return render(request, "auctions/index.html",{
        "listings":listings,
        
    })

def close_listing(request):
    listings=Listing.objects.filter(status="sold")
    winner=request.user
    return render(request, "auctions/index.html",{
            "listings":listings,
            "close":"close",
            "win_message": "Congratulations, you won this auction",
            "winner":winner,
            })
       


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def newlisting(request):
    if request.method=="POST":
        form=ListingForm(request.POST)
        #save form as a new listing
        if form.is_valid():
            listing=form.save(commit=False)
            listing.user=request.user
            listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        form=ListingForm()
    return render (request, "auctions/newListing.html",{
        "form":form,
    }) 

def product(request,id):
    #Display listing page
    listing=Listing.objects.get(pk=id)
    bid=Bid.objects.filter(product_id=id)
    comments=Comment.objects.filter(item_id=id)
    form=BidForm
    return render (request, "auctions/product.html",{
    "listing":listing,
    "comments":comments,
    "bid":bid,
    "form":form,
    "delete": WatchList.objects.filter(user=request.user, watchlist_id=id),
})

   
@login_required
def add_comment(request,id):
    listing=Listing.objects.get(pk=id)
    comments=Comment.objects.filter(item_id=id)
    #Add comment and return listing page
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.user=request.user
            comment.save()
            return  render (request, "auctions/product.html",{
            "listing":listing,
            "comments":comments,
            })

    else:
        form=CommentForm()
    return render (request, "auctions/add_comment.html",{
         "form":form,
         "listing":listing,
    })

def categories(request):
    #Show all categories
    categories=Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories":categories,
    })

def category (request,id):
    #Display active listing which belongs to selected category 
    category=Category.objects.get(pk=id)
    listings=Listing.objects.filter(category_id=id)
    return render(request, "auctions/category.html", {
        "category":category,
        "listings":listings,
    })

def my_watchlist(request):
    listings=WatchList.objects.filter(user_id = request.user)
    return render (request, "auctions/my_watchlist.html", {
        "listings": listings,
    })

@login_required
def add_watchlist(request,id):
    listing=Listing.objects.get(pk=id)
    comments=Comment.objects.filter(item_id=id)
    # Add product to watchlist and return listing page
    if request.method=="POST":  
        watchlist=WatchList()
        watchlist.user_id=request.user.id
        watchlist.watchlist_id=id
        watchlist.save()
        return  render (request, "auctions/product.html",{
            "listing":listing,
            "comments":comments,
            "watch_message": "Successefully added to watchlist",
            "delete": WatchList.objects.filter(user=request.user, watchlist_id=id),
            })

@login_required
def delete_watchlist(request,id):
    listing=Listing.objects.get(pk=id)
    comments=Comment.objects.filter(item_id=id) 
    #Delete product from watchlist and return listing page
    if request.method=="POST": 
        watchlist=WatchList.objects.filter(watchlist_id=id)
        watchlist.delete()
        return  render (request, "auctions/product.html",{
            "listing":listing,
            "comments":comments,
            "delete_message": "Successefully deleted from watchlist"
            })

@login_required
def add_bid(request,id):
    listing=Listing.objects.get(pk=id)
    comments=Comment.objects.filter(item_id=id)
    
    #Save starting price as fist bid for prevent an error
    first_bid=Bid()
    first_bid.price=listing.starting_price
    first_bid.product_id=id
    first_bid.bidder_id=request.user.id
    first_bid.save()
    # Save user's bid as starting price
    if request.method=="POST":
        form = BidForm(request.POST)
        if form.is_valid():
                new_bid = form.save(commit=False)
                new_bid.bidder_id = request.user.id
                new_bid.product_id=id
                new_bid.listing = listing
                if new_bid.price > listing.starting_price:
                    new_bid.save()
                    listing.starting_price=new_bid.price
                    listing.save()
                    return  render (request, "auctions/product.html",{
                    "listing":listing,
                    "comments":comments,
                    "form":form,
                    
                })
                else:
                    return  render (request, "auctions/product.html",{
                    "listing":listing,
                    "comments":comments,
                    "form":form,
                    "error_message": "Your bid must be higher than the current bid"
                
                })     
    else:
        form = BidForm()
        return  render (request, "auctions/product.html",{
                    "listing":listing,
                    "comments":comments,
                    "form":form,        
            })

def my_page(request):
    listings=Listing.objects.filter(user_id=request.user.id)
    return render(request,"auctions/my_page.html",{
        "listings":listings
    })

@login_required
def sell(request,id):
    #Sell the product to highest bidder
    if request.method=="POST":
        listing=Listing.objects.get(pk=id)
        starting_price=listing.starting_price
        bid_list=Bid.objects.filter(product_id=id)
        highest_bid=bid_list.get(price=starting_price)
        listing.winner_id=highest_bid.bidder_id
        listing.status="sold"
        listing.save()        
        return HttpResponseRedirect(reverse("my_page"))

