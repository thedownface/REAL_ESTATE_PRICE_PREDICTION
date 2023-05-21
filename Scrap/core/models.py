from django.db import models
from django.conf import settings
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255,default='')

    def __str__(self):
        return self.name

class Item(models.Model):
    title=models.CharField(max_length=100,default='')
    image=models.ImageField(upload_to='product_images',null=True)
    price=models.FloatField(default=0)
    predicted_price=models.FloatField(default=0)
    description=models.CharField(max_length=200,default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default='')
    slug=models.SlugField(default='')

    
    
    def get_absolute_url(self):
        return reverse('core:product',kwargs={
            'slug':self.slug
        })

    def get_add_to_cart_url(self):
         return reverse('core:add_to_cart',kwargs={
            'slug':self.slug
        })
    def get_remove_from_cart_url(self):
         return reverse('core:remove_from_cart',kwargs={
            'slug':self.slug
        })


    


    def __str__(self):
        return self.title
    
    def get_total_price(self):
        return int(self.price * self.weight)
    

class OrderItem(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=100)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    ordered=models.BooleanField(default=False)
    ordered_date=models.DateTimeField()

    def __str__(self):
        return self.user.username
    
  
