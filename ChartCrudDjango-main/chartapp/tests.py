from django.test import TestCase
from chartapp.models import Product
import chartapp.views

class ProductTestClass(TestCase):
    def setUp(self):       
        Product.objects.create(id=30, category="Kurczak",num_of_products=32, date_of_last_one='2023-05-29 10:06:08.338067')
    def test_1(self):
        chicken = Product.objects.get(id=30)
        self.assertEqual(chicken.num_of_products,32)
       
        
    def test_2(self):
        chicken = Product.objects.get(id=30)


        #self.assertEqual(chicken.num_of_products,32)
        self.assertEqual(chicken.num_of_products,32)
        


# Create your tests here.
