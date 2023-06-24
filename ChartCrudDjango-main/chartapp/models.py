from django.db import models
from datetime import datetime
# Create your models here.
import pytz
from django.utils import timezone
timez = pytz.timezone('Europe/Berlin')
class Product(models.Model):
    category = models.CharField(max_length=100, null=False, blank=False)
    full_category_name = models.CharField(max_length=100,blank=True)
    num_of_products = models.IntegerField()
    date_of_last_one = models.DateTimeField(blank=True, default=datetime.now())


    def __str__(self):
        return f'{self.category} - {self.full_category_name} - {self.num_of_products} - {self.date_of_last_one}'
        
class Logs(models.Model):
    date_of_event = models.DateTimeField(blank=True, default=datetime.now())
    logString = models.CharField(max_length=100,blank=True)
    product_id = models.IntegerField(max_length=100, default=None)
    event_Type = models.CharField(max_length=100,blank=True)

   # def logEvent(self,logString,date_of_event,event_Type):
    #    self.logString =  logString
    #    self.date_of_event = date_of_event
    #    self.event_Type = event_Type
    #    self.id
    #    self.save()

        
    def __str__(self):
        return f'{self.date_of_event} - {self.logString} - {self.event_Type} - {self.product_id}'