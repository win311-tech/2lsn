from django.db import models
from django.contrib.auth.models import User



class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quality = models.CharField(max_length=50)
    stock = models.PositiveIntegerField()

def __str__(self):
    return self.name     


class UserProfile(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    order = models.ManyToManyField(Product)
    transaction = models.CharField(max_length=100, blank=True)
    Orderhistory_id = models.CharField(max_length=100, blank=True)  
    joined_date = models.DateTimeField(auto_now_add=True)
    Preference = models.CharField(max_length=100, blank=True)
    Favorite_product = models.CharField(max_length=100, blank=True)
    
    
    
    def __str__(self):
        return self.user.username  
    

class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    Product = models.ManyToManyField(Product)
    Cart = models.ManyToManyField(Product, related_name='cart_products')
    type = models.CharField(max_length=50)
    Logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True)
    BnnnerImage = models.ImageField(upload_to='shop_banners/', blank=True, null=True)   
    
class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Number = model.PositiveIntegerField(default=0)
    CartItem = model.CharField(max_length=100, blank=True)  
    
    
    
class CartItem(models.Model):
    id = models.AutoField(primary_key=True) 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    
class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    address = models.CharField(max_length=255)
    Order = model.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=20)
    


class OrderHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_status = models.BooleanField(default=False)
    Orderhistory_id = models.CharField(max_length=100, blank=True)
    PaymentMade = models.DateTimeField(auto_now_add=True)
    OrderItem = models.CharField(max_length=100, blank=True)
    
    
    
class OrderItem(models.Model):
    id = models.AutoField(primary_key=True) 
    order_history = models.ForeignKey(OrderHistory, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True)
    
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_history = models.ForeignKey(OrderHistory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    PaymentMethod = models.CharField(max_length=50, blank=True)
    
class PaymentMethod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)  
    token = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=True)
    currency = models.CharField(max_length=10, blank=True)
    owner_id = models.CharField(max_length=100, blank=True)
    
    
class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_history = models.ForeignKey(OrderHistory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_status = models.BooleanField(default=False)
    transaction_date = models.DateTimeField(auto_now_add=True)
    PaymentMethod = models.CharField(max_length=50, blank=True)
    