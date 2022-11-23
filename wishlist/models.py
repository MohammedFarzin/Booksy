from django.db import models
from store.models import Product,Variation
from authentication.models import Account


# Create your models here.

class Wishlist(models.Model):
    wishlist_id=models.CharField(max_length=250, blank=True)
    date_added=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.wishlist_id


class WishlistItems(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    wishlist=models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True)
    is_active=models.BooleanField(default=True)


    def __unicode__(self):
        return self.product

    
    
    
    class Meta:
        verbose_name = 'wishlist items'
        verbose_name_plural = 'wishlist items'


