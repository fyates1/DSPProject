from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, CSVUploadForm, ActiveItemForm, StockItemForm, WriteOffForm, moveProductForm
from .models import Product, ActiveProduct, StockItem, WriteOff, sequence
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db import models
import random
import csv
import io
def storeManagerOnly(function):
    def wrap(request,*args,**kwargs):
        if not request.user.is_authenticated or not request.user.is_StoreManager:
            messages.error(request,"You can't access this page!")
            return redirect('home')
        return function(request, *args,**kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def managerOnly(function):
    def wrap(request,*args,**kwargs):
        if not request.user.is_authenticated or not (request.user.is_Manager or request.user.is_StoreManager):
            messages.error(request,"You can't access this page!")
            return redirect('home')
        return function(request, *args,**kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

@login_required(login_url="/login/")
def home(request):
    return render(request,"Inventory_home.html")

@login_required(login_url="/login/")
@storeManagerOnly
def bulk_add_products(request):
    if request.method=='POST':
        form=CSVUploadForm(request.POST,request.FILES)
        if form.is_valid():
            file=request.FILES['file']
            if file.name.endswith('.csv'):
                data = file.read().decode('utf-8')
                reader = csv.reader(io.StringIO(data))
                count=0
                for row in reader:               
                    if count!=0:
                        product = Product(ProductName=row[1],
                        Brand=row[2],
                        Price=row[3],
                        DiscountPrice=row[4],
                        Image_Url=row[5],
                        Category=row[6],
                        Barcode=row[8],
                        EAN=row[9])
                        product.save()
                    count+=1
                return redirect('Inventory:home')
            else:
                form.add_error("file","Please only upload CSV's")
    else:
        form = CSVUploadForm()
    return render(request,"bulk_add_products.html",{"form":form})

@login_required(login_url="/login/")
@storeManagerOnly
def add_product(request):
    submitted = False
    if request.method=="POST":
        form = ProductForm()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/inv/add_product?submitted=True")
    else:
        form = ProductForm
        if submitted in request.GET:
            submitted=True
    return render(request,"add_product.html",{"form":form,"submitted":submitted})

@login_required(login_url="/login/")
@storeManagerOnly
def product_list(request):
    product_list= Product.objects.all()
    query = request.GET.get("q")
    if query:
        product_list = product_list.filter(ProductName__icontains=query)
    paginator = Paginator(product_list,27)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    Categories = list(Product.objects.order_by().values_list('Category',flat=True).distinct())
   
    return render(request,"product_list.html",{"products":products,"Categories":Categories,"query":query})

@login_required(login_url="/login/")
def show_product(request,product_id):
    product = Product.objects.get(pk=product_id)
    return render(request,"product.html",{"product":product})


@login_required(login_url="/login/")
@storeManagerOnly
def add_product_to_store(request,product_id):
    product = Product.objects.get(pk=product_id)

    if request.method=="POST":
        form = ActiveItemForm(request.POST)

        if form.is_valid():
            Item = ActiveProduct(Product=product,
            minimumStockQuantity=form.cleaned_data.get("minimumStockQuantity"),
            Class=form.cleaned_data.get("Class"))
            Item.save()
        return redirect('Inventory:product_list')
            
    else:
        form = ActiveItemForm()
        return render(request,"AddActiveProduct.html",{"product":product,"form":form})

@login_required(login_url="/login/")
@managerOnly
def view_orders(request):
    if request.method=="POST":
        item_id = request.POST["product_id"]
        quantity = request.POST["product_OrderAmmount"]

        delivery = StockItem(activeProduct=ActiveProduct.objects.get(Product=Product.objects.get(pk=item_id)),quantity=quantity)
        delivery.save()
        messages.success(request,"Delivery confirmed")
        return redirect("Inventory:view_orders")
    orders = []
    ActiveProducts= ActiveProduct.objects.all()
    for product in ActiveProducts:
        if product.get_stock() < product.minimumStockQuantity:
            orders.append({"id":product.Product.id,"ProductName":product.Product.ProductName,
            "ProductStock":product.get_stock(),"minStock":product.minimumStockQuantity,
            "OrderAmmount":((product.minimumStockQuantity-product.get_stock())+10)})

    return render(request,"orders.html",{"orders":orders})
@login_required(login_url="/login/")
def list_active_products(request):
    product_list= ActiveProduct.objects.all()
    paginator = Paginator(product_list,27)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    
    return render(request,"ActiveProducts.html",{"products":products})
@login_required(login_url="/login/")
def addStockItem(request,product_id):
    product = ActiveProduct.objects.get(Product=product_id)

    if request.method=="POST":
        form = StockItemForm(request.POST)

        if form.is_valid():
            Item = StockItem(activeProduct=product,
            bestBeforeDate=form.cleaned_data.get("bestBeforeDate"),
            quantity=form.cleaned_data.get("quantity"))
            Item.save()
        return redirect('Inventory:list_active_products')
            
    else:
        form = StockItemForm()
        return render(request,"addStock.html",{"product":product,"form":form})

@login_required(login_url="/login/")
@managerOnly
def view_inventory(request):
    products = ActiveProduct.objects.all()
    total_units = sum(product.get_stock() for product in products)
    total_value=sum(product.Product.Price * product.get_stock() for product in products)
    return render(request,"viewStock.html",{"stock":products, "total_units":total_units,"total_value":total_value})


@login_required(login_url="/login/")
def writeoff(request):
    if request.method=="POST":
        item_id = request.POST["item_id"]
        quantity = request.POST["quantity"]

        try:
            item = StockItem.objects.get(id=item_id)
        except StockItem.DoesNotExist:
            messages.error(request, "That item no longer exists")
            return redirect("Inventory:writeoff")

        if item.quantity < int(quantity):
            messages.error(request,"You tried writing off more items than exist!")
        else:
            # item.quantity -= int(quantity)
            # item.save()
            writeoff = WriteOff(item = item, quantity = quantity,reason = request.POST["reason"])
            writeoff.save()
            messages.success(request, "Items Removed")

        return redirect("Inventory:writeoff")
    form = WriteOffForm()
    items = list(StockItem.objects.all())
    for item in items:
        if item.quantity <= 0:
            items.remove(item)
    return render(request,"writeoff.html",{"items":items,"form":form})

@login_required(login_url="/login/")
@managerOnly
def view_writeOffs(request):
    writeOffs = WriteOff.objects.all()
    total_units = sum(writeoff.quantity for writeoff in writeOffs)
    total_value=sum(writeoff.item.activeProduct.Product.Price * writeoff.quantity for writeoff in writeOffs)
    return render(request,"writeoff_list.html",{"writeOffs":writeOffs, "total_units":total_units,"total_value":total_value})
@login_required(login_url="/login/")
@storeManagerOnly
def reSequenceProducts(request):
    for seq in sequence.objects.all():
        seq.delete()
    ActiveProductList = sorted(ActiveProduct.objects.all(), key= lambda m: m.Product.Category)
    x=1
    for product in ActiveProductList:
        newItem = sequence(product=product,position=x)
        newItem.save()
        x+=1
    messages.success(request,"All Items have been resequenced")
    return render(request, "ActiveProducts.html" ,{"products":ActiveProductList})

@login_required(login_url="/login/")
@managerOnly
def placeAfter(request):
    if request.method =='POST':
        form = moveProductForm(request.POST)
        if form.is_valid():
            activeProduct1 = form.cleaned_data["Product"]
            activeProduct2 = form.cleaned_data["PlaceItemAfter"]
            ap1sequence = sequence.objects.get(product=activeProduct1)
            ap2sequence = sequence.objects.get(product=activeProduct2)

            oldPos = ap1sequence.position
            newPos = ap2sequence.position
            if oldPos<newPos:
                sequences_to_update=sequence.objects.filter(position__gt=oldPos, position__lte=newPos)
                sequences_to_update.update(position=models.F('position')-1)

            else:
                sequences_to_update=sequence.objects.filter(position__gte=newPos, position__lt=oldPos)
                sequences_to_update.update(position=models.F('position')+1)

            ap1sequence.position=newPos
            ap1sequence.save()
            messages.success(request,"Move Successful")
            return render(request,'swapProducts.html',{'form':form})
    else:
        form = moveProductForm

        return render(request,'swapProducts.html',{'form':form})




    


            