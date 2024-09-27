from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import date

from .models import User, Bid, Listing, Comment
    
def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })

#################################

def listing(request, id):
    class BidForm(forms.ModelForm):
        class Meta:
            model = Bid
            fields = ["amount"]
    object = Listing.objects.get(id=f"{id}")
    if request.method == "GET":
        form = BidForm()
        if not object.bids.all():
            bid_amount = None
            minimum_bid = object.starting_price
        else:
            highest_bid = object.bids.last() 
            bid_amount = highest_bid.amount
            minimum_bid = float(bid_amount) + .25
        return render(request, "auctions/listing.html", {
            "listing": object,
            "price": bid_amount,
            "minimum_bid": minimum_bid,
            "form": form
        })
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = Bid()
            clean_form = form.cleaned_data
            if clean_form["amount"] < object.bids.first().amount:
                return render(request, "auctions/listing.html", {
                    "form": form,
                    "messages": ["Buyout price must be higher than starting bid!"]
                })
            for field in clean_form:
                setattr(bid, field, clean_form[field])
            setattr(bid, "user_id", request.user.id)
            bid.save()
        return HttpResponseRedirect(reverse("listing", args=[object.id]))

#################################
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

########################################

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#################################

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

##########################################

def new_listing(request):
    class ListingForm(forms.ModelForm):
        class Meta:
            today = date.today()
            model = Listing
            fields = ["item_name", "category", "starting_price", "buyout_price", "expiration", "description", "image"]
            widgets = {
                'expiration': forms.DateInput(attrs={'type': 'date', 'min': f'{today}'})
            }
    if request.method == "GET":
        form = ListingForm()
        return render(request, "auctions/new_listing.html", {
            "form": form
        })
    
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = Listing()
            clean_form = form.cleaned_data
            if clean_form["starting_price"] > clean_form["buyout_price"]:
                return render(request, "auctions/new_listing.html", {
                    "form": form,
                    "messages": ["Buyout price must be higher than starting bid!"]
                })
            for field in clean_form:
                setattr(listing, field, clean_form[field])
            setattr(listing, "user_id", request.user.id)
            listing.save()

        return HttpResponseRedirect(reverse("index"))
