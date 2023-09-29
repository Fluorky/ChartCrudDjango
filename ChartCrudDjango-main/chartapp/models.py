from django.db import models
from datetime import datetime
# Create your models here.
#import pytz
from django.utils import timezone
#timez = pytz.timezone('Europe/Berlin')
class Product(models.Model):
    category = models.CharField(max_length=100, null=False, blank=False)
    full_category_name = models.CharField(max_length=100,blank=True)
    num_of_products = models.IntegerField()
    date_of_last_one =  models.DateTimeField(blank=True,auto_now_add=True)

    def __str__(self):
        return f'{self.category} - {self.full_category_name} - {self.num_of_products} - {self.date_of_last_one}'
        
class Logs(models.Model):
    date_of_event = models.DateTimeField(blank=True, default=datetime.now())
    logString = models.CharField(max_length=100,blank=True)
    product_id = models.IntegerField(default=None)
    event_Type = models.CharField(max_length=100,blank=True)
    ip = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f'{self.date_of_event} - {self.logString} - {self.event_Type} - {self.product_id} - {self.ip}'


class Example_Data(models.Model):
    hours = models.CharField(max_length=100,blank = True, unique=True)
    quantity =  models.IntegerField(default=None)
    line1 =  models.IntegerField(default=None)
    line2 =  models.IntegerField(default=None)
    line3 =  models.IntegerField(default=None)
    def __str__(self):
        return f'{self.hours} - {self.quantity } - {self.line1} - {self.line2} - {self.line3}'

#class Sensors(models.Model):
   #ip = models.CharField(max_length=100,blank=True)
   # date_of_event = models.DateTimeField(blank=True, default=datetime.now())
   #parametersString = models.CharField(max_length=100,blank=True)
   #value_of_parameters = models.CharField(max_length=100,blank=True)
    