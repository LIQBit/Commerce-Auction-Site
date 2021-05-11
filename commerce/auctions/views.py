from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from datetime import datetime
from annoying.functions import get_object_or_None
from .models import User, Listing, Bids, Comments, Watchlist, Winner
from django import forms


def index(request):
    aList = Watchlist.objects.filter(user=request.user.username)
    watchlistcount = len(aList)

    return render(request, "auctions/index.html", {
        "items": Listing.objects.all(),
        "watchlistcount": watchlistcount
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

def create(request):
    aList = Watchlist.objects.filter(user=request.user.username)
    watchlistcount = len(aList)

    if request.method == "POST":
        listingTable = Listing()
        listingTable.owner = request.user.username
        listingTable.title = request.POST.get('title')
        listingTable.description = request.POST.get('description')
        listingTable.price = request.POST.get('price')
        listingTable.pic = request.POST.get('pic')
        listingTable.category = request.POST.get('category')
        listingTable.save()

        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "auctions/create.html", {
        "category": category,
        "watchlistcount": watchlistcount
    })


def listing(request, listing_id):
    comments = Comments.objects.filter(listing_id=listing_id)
    item = Listing.objects.get(pk = listing_id)
    aList = Watchlist.objects.filter(user=request.user.username)
    watchlistcount = len(aList)

    if request.method == "POST":
        watchlistcount = len(aList)
        item = Listing.objects.get(pk=listing_id)
        newBid = int(request.POST.get("bid"))
        #if bid is greater than or equal to current bid.
        if item.price >= newBid:
            thing = Listing.objects.get(pk=listing_id)
            return render(request, "auctions/listing.html", {
                "item":item,
                "message": "Bid must be higher than current bid",
                "message_type": "warning",
                "comments":comments,
                "watchlistcount": watchlistcount,
            
            })
        #if new bid is greater than current bid.
        else:
            item.price = newBid
            item.save()
            bidObject = Bids.objects.filter(listingid=listing_id)
            if bidObject:
                bidObject.delete()
            obj = Bids()
            obj.user = request.user.username
            obj.title = item.title
            obj.listingid = listing_id
            obj.bid = newBid
            obj.save()
            item = Listing.objects.get(pk=listing_id)
            
            return render(request, "auctions/listing.html", {
                "item":item,
                "message": "Bid succesful",
                "message_type": "success",        
                "comments":comments,
                "watchlistcount": watchlistcount,
                
            })


    added = Watchlist.objects.filter(listingid=listing_id, user=request.user.username)
    product = Listing.objects.get(listing_id=listing_id)   
    return render(request, "auctions/listing.html", {
        "item": item,
        "watchlistcount": watchlistcount,
        "added": added,
        "comments": comments,
    })


# display the list of categories
def categories(request):
    aList = Watchlist.objects.filter(user=request.user.username)
    watchlistcount = len(aList)
    categoryList = Listing.objects.filter(category=categories)

    return render(request,"auctions/categories.html", {
        "watchlistcount": watchlistcount,
        "categoryList": categoryList
    } )


#Display active listings in a category

def category(request, category):
    CategoryList = Listing.objects.filter(category=category)

    #categoryList = Listing.objects.filter(category = category)
    print(CategoryList)
    
    return render(request, "auctions/category.html", {
        "Categorylist": category,
        "current_category" : category
    })


def check_categories(request, category):
    aList = Watchlist.objects.filter(user=request.user.username)
    watchlistcount = len(aList)
    categorylist = Listing.objects.filter(category = category)
    
    return render(request, "auctions/category_check.html", {
        "categorylist": categorylist,
        "current_category" : category,
        "watchlistcount": watchlistcount
    
    })

        
def submitcomment(request,listing_id): 
    comments = Comments.objects.filter(listing_id=listing_id)
    item = Listing.objects.get(pk=listing_id)

    timenow = datetime.now()
    dateTime = timenow.strftime(" %d %B %Y %X ")

    obj = Comments()
    obj.comment = request.POST.get("comment")
    obj.user = request.user.username
    obj.listing_id = listing_id
    
    obj.time = dateTime
    obj.save()

  
    return redirect('listing', listing_id=listing_id)


def addwatchlist(request, listing_id):
    obj = Watchlist.objects.filter(listingid = listing_id, user=request.user.username)
    comments = Comments.objects.filter(listing_id=listing_id)
    item = Listing.objects.get(pk = listing_id)

    if obj:
        obj.delete()

        product = Listing.objects.get(listing_id=listing_id)
        added = Watchlist.objects.filter(listingid=listing_id, user=request.user.username)
        aList = Watchlist.objects.filter(user=request.user.username)
        watchlistcount = len(aList)
        return render(request, "auctions/listing.html", {
            
            "item": item,
            "Watchlistcount": watchlistcount,
            "added": added,
            "comments": comments
           
        })
    else:
        obj = Watchlist()
        obj.user = request.user.username
        obj.listingid = listing_id
        obj.save()

        product = Listing.objects.get(listing_id=listing_id)
        added = Watchlist.objects.filter(listingid=listing_id, user=request.user.username)
        aList = Watchlist.objects.filter(user=request.user.username)
        watchlistcount = len(aList)
        return render(request, "auctions/listing.html", {
           
            "item": item,
            "Watchlistcount": watchlistcount,
            "added": added,
            "comments": comments
            
        })

def watchlistpage(request):
    aList = Watchlist.objects.filter(user=request.user.username)
    watchlistcount = len(aList)

    present = False
    productlist = []
    i = 0
    if aList:
        present = True
        for item in aList:
            product = Listing.objects.get(listing_id=item.listingid)
            productlist.append(product)


    return render(request, "auctions/watchlist.html", {
        "productlist": productlist,
        "present": present,
        "watchlistcount": watchlistcount
    })

def closebid(request, listing_id):
    winobj = Winner()
    listobj = Listing.objects.get(listing_id=listing_id)
    obj = get_object_or_None(Bids, listingid=listing_id)
    aList = Watchlist.objects.filter(user=request.user.username)
    watchlistcount = len(aList)
    if not obj:
        message = "Deleting Bid"
        msg_type = "danger"
    else:
        bidobj = Bids.objects.get(listingid=listing_id)
        winobj.owner = request.user.username
        winobj.winner = bidobj.user
        winobj.listingid = listing_id
        winobj.winningprice = bidobj.bid
        winobj.title = bidobj.title
        winobj.save()
        message = "This listing is closed"
        msg_type = "success"


    #remove from the watchlist
    if Watchlist.objects.filter(listingid=listing_id):
        watchobj = Watchlist.objects.filter(listingid=listing_id)
        watchobj.delete()
    
    #remove from Comments
    if Comments.objects.filter(listing_id=listing_id):
        commentobj = Comments.objects.filter(listing_id=listing_id)
        commentobj.delete()

    #remove from Listings
    listobj.delete()

    #new list of items
    winners = Winner.objects.all()
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, "auctions/closed.html", {
        "winningobject":winobj,
        "winners": winners,
        "empty": empty,
        "message": message,
        "msg_type": msg_type,
        "watchlistcount": watchlistcount
    })

def mywinnings(request):
    winners = Winner.objects.filter(winner=request.user.username)
    L = Watchlist.objects.filter(user=request.user.username)
    watchlistcount = len(L)
    present = False
    productList = []
    i = 0
    if L:
        present = True
        for item in L:
            product = Listing.objects.get(listing_id=item.listingid)
            productList.append(item)
    

    return render(request, "auctions/mywinnings.html", {
        "product_list":productList,
        "present": present,
        "products": winners,
        "watchlistcount": watchlistcount,

    })






