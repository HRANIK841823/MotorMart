from django.db import models
from brand.models import Brand
from django.contrib.auth.models import User
# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    brand = models.ForeignKey(Brand, related_name='cars', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    car=models.ForeignKey(Car,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=30)
    email=models.EmailField()
    body=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comments by {self.name}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ordered {self.car.name}"
