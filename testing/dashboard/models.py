from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
class Product(models.Model):
    shape = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class User(models.Model):
    name= models.CharField(max_length=100)   
    username  = models.CharField(max_length=100)
    password  = models.CharField(max_length=100 , default='default_password')
    age= models.IntegerField()   
    address= models.CharField(max_length=200)   

class Recommendation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    