from django import forms

from .models import Listing, Comment,Bid

class ListingForm (forms.ModelForm):
    class Meta:
        model=Listing
        fields=["title","description", "image","starting_price", "category",]

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=["subject", "entry","item"]

class BidForm(forms.ModelForm):
    class Meta:
        model=Bid
        fields=["price"]