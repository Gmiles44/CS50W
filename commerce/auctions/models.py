from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}: {self.id}"
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    item_name = models.CharField(max_length=64)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    buyout_price = models.DecimalField(max_digits=12, decimal_places=2)
    expiration = models.DateTimeField()
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.item_name}, posted by {self.user.username}"

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")

class Comment(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    time = models.DateTimeField(auto_now_add=True)