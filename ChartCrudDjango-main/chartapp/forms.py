from django import forms
from . models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
          #  'id': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'full_category_name': forms.TextInput(attrs={'class': 'form-control'}),
            'num_of_products': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_last_one': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }



class MyForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    a = forms.CharField(max_length=20)
    a2 = forms.CharField(max_length=20)
    #b = forms.CharField(max_length=20)
    #c = forms.CharField(max_length=20)