from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Listing(models.Model):
    listing_id = models.AutoField(primary_key=True,)
    owner = models.CharField(max_length=64,)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=300, blank=True, null=True)
    price = models.IntegerField(null=True)
    category = models.CharField(max_length=64)
    link = models.CharField(max_length=64, default=None, blank=True, null=True)
    pic = models.URLField(max_length=200, default=None, blank=True, null=True)


  


class Bids(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.IntegerField()


class Comments(models.Model):
    user = models.CharField(max_length=60)
    comment = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    listing_id = models.IntegerField()

class Watchlist(models.Model):
    user = models.CharField(max_length=70)
    listingid = models.IntegerField()


class Winner(models.Model):
    owner = models.CharField(max_length=70)
    winner = models.CharField(max_length=70)
    listingid = models.IntegerField()
    winningprice = models.IntegerField()
    title = models.CharField(max_length=80, null=True)