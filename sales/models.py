from django.db import models

#Staff table, use for track all sales staff
#commission is an integer,when somebody's commission is 10,this employee get 10% from sales.it might not a friendly way to store data
class Staff(models.Model):
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    commission = models.IntegerField(default=0)
    def __str__(self):
        return self.name
#Beverage table, Use to store beverages and their prices
class Beverage(models.Model):
    Beverage_text = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    def __str__(self):
        return self.Beverage_text

#Record table, Used to record sales forms uploaded by staff
class Record(models.Model):
   name = models.CharField(max_length=50) 
   Beverage_text = models.CharField(max_length=50)
   pub_date = models.DateTimeField('date published')
   quantity = models.IntegerField(default=0)
   def __str__(self):
        return self.name

#Username and password table
class User(models.Model):
    username=models.CharField(max_length=32)
    password=models.CharField(max_length=32)
    def __str__(self):
        return self.username