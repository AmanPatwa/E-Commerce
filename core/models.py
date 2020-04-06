from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

CATEGORY_CHOICES = {
    ('S','Shirt'),
    ('SW','Sport wear'),
    ('OW','Outwear')
}

LABEL_CHOICES = {
    ('P','primary'),
    ('S','secondary'),
    ('D','danger'),
    ('I','info')
}

class Item(models.Model):
    title = models.CharField(max_length = 100)
    price = models.FloatField()
    discount_price = models.FloatField(blank = True, null = True)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices = LABEL_CHOICES, max_length=1)
    description = models.TextField()
    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:product',kwargs={'pk':self.pk})

    def get_add_to_cart_url(self):
        return reverse('core:add-to-cart',kwargs={'pk':self.pk})

    def get_remove_from_cart_url(self):
        return reverse('core:remove-from-cart',kwargs={'pk':self.pk})

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete = models.CASCADE)
    item = models.ForeignKey(Item,on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)
    ordered = models.BooleanField(default = False)

    def __str__(self):
        return str(self.quantity) + ' of ' +  self.item.title

    def get_price(self):
        if self.item.discount_price:
            return self.item.discount_price
        return self.item.price

    def get_total_price(self):
        price = self.get_price()
        return self.quantity * price

    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default = False)
    billing_address = models.ForeignKey('BillingAddress',on_delete = models.SET_NULL, blank=True, null = True)

    def __str__(self):
        return self.user.username

    def get_order_total_price(self):
        total = 0
        for item in self.items.all():
            total += item.get_total_price()
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete = models.CASCADE)
    street_address = models.CharField(max_length=50)
    appartment_address = models.CharField(max_length=50)
    country = CountryField(multiple = False)
    zip = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username