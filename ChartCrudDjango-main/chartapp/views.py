import time
from zoneinfo import ZoneInfo
from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404,HttpResponseRedirect
from . models import Product, Logs, Example_Data
from . forms import MyForm, ProductForm
from datetime import datetime
from django.utils import timezone
import pytz
from django.core import serializers
from django.db.models import Sum
import subprocess
from pymodbus.client import ModbusTcpClient
from pymodbus.register_read_message import ReadHoldingRegistersResponse
import ipaddress


timez = pytz.timezone('Europe/Berlin')
global addr
global addr2
global a
global b

addr= "192.168.2.1"
addr2= "192.168.2.2"
a=1
b=2

def home(request):
    products = Product.objects.all()
    
    for model in products:
     model.date_of_last_one= model.date_of_last_one.astimezone(ZoneInfo('Europe/Berlin'))
     model.date_of_last_one= model.date_of_last_one.strftime("%Y-%m-%d %H:%M:%S")

    context = {
        "products": products,
      
    }
    return render(request, 'chartapp/index.html',context)

def mock_chart(request):
    data = Example_Data.objects.all()

    context = {
        "hours": data.model.hours,
        "quantity" : data.model.quantity,
        "line1": data.model.line1,
        "line2": data.model.line2,
        "line3": data.model.line3 ,

      
    }
    return render(request, 'chartapp/charts.html',context)

def chart(request):
    products = Product.objects.all()
    
    context = {
        "products": products,
    }

    return render(request, 'chartapp/ind.html', context)




def chartJson(request):

    SomeModel_json = serializers.serialize("json", Product.objects.all())
    data = {"xD": SomeModel_json}
    return JsonResponse(data)

    
   
def products_chart(request):
    id = []
    labels = []
    data = []
    full_category_name = []
    date_of_last_one = []
    
    q=Product.objects.values_list('category').values()
    for entry in q:
       
        id.append(entry['id'])
        labels.append(entry['category'])
        data.append(entry['num_of_products'])
        full_category_name.append(entry['full_category_name'])
        date_last=entry['date_of_last_one']
        date_last= date_last.astimezone(ZoneInfo('Europe/Berlin'))
        date_last = date_last.strftime("%Y-%m-%d %H:%M:%S")
        date_of_last_one.append(str(date_last))
     
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
            
            log = str(form['full_category_name'].value()) +" total "+ str(form['num_of_products'].value())
            logging= Logs(logString=log,date_of_event= datetime.now(tz=timez),event_Type="Add", product_id=products.count(),ip=get_client_ip(request))
            logging.save()
            return redirect('index')
    else:
        form = ProductForm()        

    context = {
        "products": products,
        "form": form
    }
      
    return render(request, 'chartapp/add_view.html', context)

def addOne(request,id):
    # 
    context ={}
 
    obj = get_object_or_404(Product, id = id)
    
    if request.method =="POST":
        obj.num_of_products=obj.num_of_products+1
        obj.date_of_last_one = datetime.now(tz=timez) 
        log = str(obj.full_category_name) +" total "+ str(obj.num_of_products)
        obj.save()
        logging= Logs(logString=log,date_of_event= obj.date_of_last_one,event_Type="Iterator", product_id=obj.pk,ip=get_client_ip(request))
        logging.save()
      
    return render(request, "chartapp/update_view.html", context)    

def list_view(request):

    context ={}
    context["dataset"] = Product.objects.all()
         
    return render(request, "chartapp/list_view.html", context)

def detail_view_by_name(request, category):
 
    context ={}
    context["data"] = Product.objects.filter(category=category)
         
    return render(request, "chartapp/detail_view_by_name.html", context)
def detail_view(request, id):


    context ={}   
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
        return HttpResponseRedirect("/"+str(id))
 
    log = str(obj.full_category_name) +" total "+ str(obj.num_of_products)
    logging= Logs(logString=log,date_of_event= datetime.now(tz=timez) ,event_Type="Update", product_id=obj.pk,ip=get_client_ip(request))
    logging.save() 

    context["form"] = form
 
    return render(request, "chartapp/update_view.html", context)


def resetOne(request,id):
    
    context ={}

    obj = get_object_or_404(Product, id = id)
 
    if request.method =="POST":
        obj.num_of_products=0
        obj.date_of_last_one = datetime.now(tz=timez)
        obj.save()
        log = str(obj.full_category_name) +" total "+ str(obj.num_of_products)
        logging= Logs(logString=log,date_of_event= datetime.now(tz=timez) ,event_Type="ResetOne", product_id=obj.pk,ip=get_client_ip(request))
        logging.save()
    return render(request, "chartapp/reset_one_view.html", context)    

def reset_view(request):

    context ={}  
    context["dataset"] = Product.objects.update(num_of_products=0)
    log = str("All products are reseted")
    logging= Logs(logString=log,date_of_event= datetime.now(tz=timez) ,event_Type="ResetAll", product_id=0,ip=get_client_ip(request))
    logging.save()
    return render(request, "chartapp/reset_view.html", context)

def delete_view(request, id):

    context ={}

    obj = get_object_or_404(Product, id = id)
 
    if request.method =="POST":
        log = str(obj.full_category_name) +" total "+ str(obj.num_of_products)
        logging= Logs(logString=log,date_of_event= datetime.now(tz=timez) ,event_Type="Detele", product_id=obj.pk,ip=get_client_ip(request))
        logging.save()
        obj.delete()
    
        return HttpResponseRedirect("/")
 
    return render(request, "chartapp/delete_view.html", context)


def log_list_view(request):

    context ={}
    context["dataset"] = Logs.objects.all().order_by("-id")
         
    return render(request, "chartapp/logs_list_view.html", context)


def ping_list_view(request):

    context ={}
    #context["dataset"] = Logs.objects.all().order_by("-id")
         
    return render(request, "chartapp/ip_list_view.html", context)


def logs_update(request):
  
    id = []
    product_id = []
    logString  = []
    event_Type = []
    date_of_event = []
    ip = []
    
    #x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #if x_forwarded_for:
    #    ipik = x_forwarded_for.split(',')[-1].strip()
    #else:
    #    ipik = request.META.get('REMOTE_ADDR')
    
    #print(ipik)

    q=Logs.objects.values_list('product_id').values()
    for entry in q:
       
        id.append(entry['id'])
        product_id.append(entry['product_id'])
        logString.append(entry['logString'])
        event_Type.append(entry['event_Type'])
        
        d=entry['date_of_event']
        d= d.astimezone(ZoneInfo('Europe/Berlin'))
        d = d.strftime("%Y-%m-%d %H:%M:%S")
        
        date_of_event.append(str(d))
        ip.append(entry['ip'])
    
     
    return JsonResponse(data={
        'id': id,
        'product_id': product_id,
        'logString': logString,
        "event_Type" :  event_Type,
        "date_of_event": date_of_event,
        "ip": ip,

    })


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def validate_ip_address(ip_string):
   try:
       ip_object = ipaddress.ip_address(ip_string)
       print("The IP address",ip_object,"is valid.")
       return True
   except ValueError:
       print("The IP address", ip_object ,"is valid.")
       return False

def ping_ip(ip):

    (output, error) = subprocess.Popen((['ping',ip,'-n','1']),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,close_fds=True).communicate()

    if b'bytes=32' in output:
        return "Work"
    elif b'Destination host unreachable.' in output:
        return "Host not response"
    elif error:
        return "DNS Error"
    else:
        return "Unknown error"
    

def ip_scanner(request):
        #addr = input("Write 3 first octets ip addres like XXX.XXX.XXX. : ")
        #a = input("Write start scanning adres between 1 and 255: ")
        #b = input("Write end scanning adres between 1 and 255: ")
        
    # a = 1
        #b = 5
        #file = "Documents/python/pingHosts.txt"
        
        id = [] 
        ips = []
        testresult= []
        #f = open(file, "w")

        
        ids = 0
        #print(addr)



        #test2 =".".join(addr2.split('.')[0:-1])
        local_addr = addr
        local_addr2 = addr2
    #if(validate_ip_address(local_addr)==True and validate_ip_address(local_addr2)==True):
        address =".".join(local_addr.split('.')[0:-1])
        print(validate_ip_address(local_addr))
        test =local_addr.split('.')[-1]
        #print(test)
        test2 =local_addr2.split('.')[-1]
    # print(test3)
    #print(addr2)
        ##test2 =addr2.split('.')[-1]
    # print(test2)

    # print(a, b)
    #  print()
        #aa=a[-3:].lstrip('.')
        #bb=b[-3:].lstrip('.')
        print(test, test2) 
        #for ip in range(int(a),int(b)+1):
        for ip in range(int(test),int(test2)+1):  
            #print(test, test2)  
            ip =str(address)+"."+str(ip)
            ip = ip.strip('\n')
            print(ip)
            response= ping_ip(ip)
            
            #result = ('%s, %s \n' %(ip,response))
            id.append(ids)
            ips.append(ip)
            testresult.append(response)
            ids=ids+1
            #print(result)
            #f.write(str(result))
   # else:
            #local_addr =local_addr.strip('\n')
            #print(local_addr)
           # response= ping_ip(local_addr)
                
                #result = ('%s, %s \n' %(ip,response))
           # id.append(ids)
           # ips.append(addr)
           # testresult.append(response)
           # ids=ids+1
    

        return JsonResponse(data={
            'id': id,
            'ips': ips,
            'testresult': testresult,
        

    })



def form_handle(request):
    context = {}
    form = MyForm()
    if request.method=='POST':
        form = MyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #now in the object cd, you have the form as a dictionary.
            #x = cd.get('a')
            #y= cd.get('b')
            #z = cd.get('c')

            global addr
            addr = cd.get('a')
            global addr2 
            addr2 = cd.get('a2')
            #global a
            #a= cd.get('b')
            #global b
            #b=cd.get('c')
            #print(str(a)+str(b)+str(c)+"DUPA")

            return HttpResponseRedirect("/pings")
        
    return render(request, "chartapp/check.html", context) 


def modbusSensors(request,ip):
  
    client = ModbusTcpClient(ip,502)
    client.connect()
    ips = []
    testresult= []
    #client.write_coil(1, True)
    #regs = client.read_holding_registers(0x0030, 5,1)
    chk = client.read_holding_registers(0x0030, 5, unit = 1)
    #response = client.execute(chk)
    #print ( response)
    #print(chk)
    #print(chk.registers)

    response= ping_ip(ip)
    print(response)  
        #result = ('%s, %s \n' %(ip,response))
    ips.append(ip)
    testresult.append(response)
    if isinstance(chk, ReadHoldingRegistersResponse):
        print (chk.registers)
    #print (regs[1])


    client.close()


    return JsonResponse(data={
        
      "registers" : chk.registers,
      'ips': ips,
      'testresult': testresult
       

    })

def sensors(request):
     return render(request, "chartapp/sensors.html") 