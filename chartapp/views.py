import time
from zoneinfo import ZoneInfo
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from . models import Product, Logs
from . forms import ProductForm
from datetime import datetime
from django.utils import timezone
import pytz
from django.core import serializers
from django.db.models import Sum
# Create your views here.
timez = pytz.timezone('Europe/Berlin')
#testowy = Logs() 

#def chart(request):
    #products = Product.objects.all()
   # context = {
      #  "products": products,
     #  # "form": form
    #}

    #return render(request, 'chartapp/index.html', context)

#def autoUpdate(request):
 #   products = Product.objects.all()
  #  context = {
   #     "products": products,
     #  # "form": form
   # }

    #return JsonResponse(context)

def home(request):
    products = Product.objects.all()
    #print(products.values())
    
    for model in products:
     model.date_of_last_one= model.date_of_last_one.astimezone(ZoneInfo('Europe/Berlin'))
     model.date_of_last_one= model.date_of_last_one.strftime("%Y-%m-%d %H:%M:%S")
     #model.save()
     
    #print(products.values('date_of_last_one'))

    context = {
        "products": products,
       # "form": form
    }
    #return render(request, 'chartapp/home.html',context)
    return render(request, 'chartapp/index.html',context)

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
    #SomeModel_json = serializers.serialize("json", Product.objects.all())
    #data = {"xD": SomeModel_json}
    #return JsonResponse(data)

    #return render(request, 'chartapp/index.html', context)
    return render(request, 'chartapp/ind.html', context)

def chartJson(request):
   #products = Product.objects.all()

   # if request.method == 'POST':
   #     form = ProductForm(request.POST)
   #     if form.is_valid():
   #         form.save()
   #         return redirect('index')
   # else:
   #     form = ProductForm()        

    #context = {
       # "products": products,
     #  # "form": form
    #}
    SomeModel_json = serializers.serialize("json", Product.objects.all())
    data = {"xD": SomeModel_json}
    return JsonResponse(data)

    
   
def products_chart(request):
    id = []
    labels = []
    data = []
    full_category_name = []
    date_of_last_one = []
    
    #queryset = Product.objects.values('category').annotate(num_of_products=Sum('num_of_products'))#.order_by('-num_of_products') 
    q=Product.objects.values_list('category').values()
    for entry in q:
       
        id.append(entry['id'])
        labels.append(entry['category'])
        data.append(entry['num_of_products'])
        full_category_name.append(entry['full_category_name'])
        #xd = entry['date_of_last_one'] - datetime.timedelta(seconds = time.timezone)
        xd=entry['date_of_last_one']
        xd= xd.astimezone(ZoneInfo('Europe/Berlin'))
        xd = xd.strftime("%Y-%m-%d %H:%M:%S")
        
        #date_of_last_one.append(str(entry['date_of_last_one']))
        #date_of_last_one.append(entry['date_of_last_one'])
        date_of_last_one.append(str(xd))
        #print(date_of_last_one)

        
     
    return JsonResponse(data={
        'id': id,
        'labels': labels,
        'data': data,
        "full_category_name" :  full_category_name,
        "date_of_last_one": date_of_last_one,

    })



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

def addOne(request,id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Product, id = id)
    
    if request.method =="POST":
        #obj.category="Linia nr 5"
        obj.num_of_products=obj.num_of_products+1
        #print(str(datetime.now))
        obj.date_of_last_one = datetime.now(tz=timez) #"2023-05-29 09:57:30.906518"#datetime.strptime(str(datetime.now()),"YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
        #testowy.logString =  str(obj.full_category_name) +" total "+ str(obj.num_of_products)
        log = str(obj.full_category_name) +" total "+ str(obj.num_of_products)
        #testowy.date_of_event = obj.date_of_last_one
        #testowy.event_Type = "AddOne"
        #testowy.save()
        obj.save()
        #testowy.logEvent(log,obj.date_of_last_one,"AddOne", id=obj.id)
        logging= Logs(logString=log,date_of_event= obj.date_of_last_one,event_Type="AddOne", product_id=obj.id)
        logging.save()
        #return HttpResponseRedirect("/")
    return render(request, "chartapp/update_view.html", context)    

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
        return HttpResponseRedirect("/"+str(id))
 
    # add form dictionary to context
    #testowy.logEvent(,,"Update")
    context["form"] = form
 
    return render(request, "chartapp/update_view.html", context)


def resetOne(request,id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Product, id = id)
 
    if request.method =="POST":
        obj.num_of_products=0
        #print(str(datetime.now))
        obj.date_of_last_one = datetime.now(tz=timez) #"2023-05-29 09:57:30.906518"#datetime.strptime(str(datetime.now()),"YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]")
        obj.save()
        #return HttpResponseRedirect("/")
    return render(request, "chartapp/reset_one_view.html", context)    

def reset_view(request):

    context ={}  
    context["dataset"] = Product.objects.update(num_of_products=0)

    return render(request, "chartapp/reset_view.html", context)

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


def log_list_view(request):

    context ={}
    context["dataset"] = Logs.objects.all()   
         
    return render(request, "chartapp/logs_list_view.html", context)
