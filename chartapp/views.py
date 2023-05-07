from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from . models import Product
from . forms import ProductForm

# Create your views here.

def chart(request):
    products = Product.objects.all()

   # if request.method == 'POST':
   #     form = ProductForm(request.POST)
   #     if form.is_valid():
   #         form.save()
   #         return redirect('index')
   # else:
   #     form = ProductForm()        

    context = {
        "products": products,
       # "form": form
    }

    return render(request, 'chartapp/index.html', context)

def addData(request):
    products = Product.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProductForm()        

    context = {
        "products": products,
        "form": form
    }
    #chart(request)
    return render(request, 'chartapp/add_view.html', context)

def list_view(request):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["dataset"] = Product.objects.all()
         
    return render(request, "chartapp/list_view.html", context)

def detail_view_by_name(request, category):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["data"] = Product.objects.filter(category=category)
    #context["data"] = Product.objects.get(id = id)
         
    return render(request, "chartapp/detail_view_by_name.html", context)
def detail_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
   
    context["data"] = Product.objects.get(id = id)
         
    return render(request, "chartapp/detail_view.html", context)

def update_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Product, id = id)
 
    # pass the object as instance in form
    form = ProductForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        #chart(request)
        return HttpResponseRedirect("/"+id)
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "chartapp/update_view.html", context)

def delete_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Product, id = id)
 
 
    #if request.method =="DELETE": it is't correct, but it works 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")
 
    return render(request, "chartapp/delete_view.html", context)