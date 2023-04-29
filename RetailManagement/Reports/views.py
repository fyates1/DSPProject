from django.shortcuts import render
from Inventory.models import WriteOff,Product,ActiveProduct,sequence,StockItem
from Inventory.views import managerOnly, storeManagerOnly
import operator
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required
@login_required(login_url="/login")
@storeManagerOnly
def home(request):

    #Most Written Off lines
    writeoffs = WriteOff.objects.all()
    writeoff_counts={}
    for item in writeoffs:
        if str(item.item.activeProduct.Product.ProductName) not in writeoff_counts.keys():
            writeoff_counts[str(item.item.activeProduct.Product.ProductName)] = item.quantity
        else:
            writeoff_counts[str(item.item.activeProduct.Product.ProductName)] += item.quantity

 
    newA = dict(sorted(writeoff_counts.items(), key=operator.itemgetter(1), reverse=True)[:5])

    
    c = ['red', 'yellow', 'black', 'blue', 'orange']
    fig = plt.figure(figsize=(10,7))
    plt.barh(range(len(newA)), list(newA.values()), align='center', color =c)
    plt.yticks(range(len(newA)), list(newA.keys()))
    plt.subplots_adjust(left=0.4)
    plt.savefig("static\images\WriteOff-graph.png")

    #Most Written Off for BBD
    writeoffsBBD = WriteOff.objects.all()
    writeoffBBD_counts={}
    for item in writeoffsBBD:
        if str(item.item.activeProduct.Product.ProductName) not in writeoffBBD_counts.keys() and item.reason == "BBD":
            writeoffBBD_counts[str(item.item.activeProduct.Product.ProductName)] = item.quantity
        elif item.reason == "BBD":
            writeoffBBD_counts[str(item.item.activeProduct.Product.ProductName)] += item.quantity


    newB = dict(sorted(writeoffBBD_counts.items(), key=operator.itemgetter(1), reverse=True)[:5])

    
    c = ['red', 'yellow', 'black', 'blue', 'orange']
    fig = plt.figure(figsize=(10,7))
    plt.barh(range(len(newB)), list(newB.values()), align='center', color =c)
    plt.yticks(range(len(newB)), list(newB.keys()))
    plt.subplots_adjust(left=0.4)
    plt.savefig("static\images\WriteOffBBD-graph.png")
#Top 5 Write Offs for damages
    writeoffsDamages = WriteOff.objects.all()
    print(writeoffsDamages)
    writeoffDamages_counts={}
    for item in writeoffsDamages:
        if str(item.item.activeProduct.Product.ProductName) not in writeoffDamages_counts.keys() and item.reason == "DAMAGES":
            writeoffDamages_counts[str(item.item.activeProduct.Product.ProductName)] = item.quantity
        elif item.reason == "DAMAGES":
            writeoffDamages_counts[str(item.item.activeProduct.Product.ProductName)] += item.quantity

    print(writeoffDamages_counts)
    newC = dict(sorted(writeoffDamages_counts.items(), key=operator.itemgetter(1), reverse=True)[:5])
    print(newC)
    
    c = ['red', 'yellow', 'black', 'blue', 'orange']
    fig = plt.figure(figsize=(10,7))
    plt.barh(range(len(newC)), list(newC.values()), align='center', color =c)
    plt.yticks(range(len(newC)), list(newC.keys()))
    plt.subplots_adjust(left=0.4)
    plt.savefig("static\images\WriteOffDamages-graph.png")

#Items Out of stock and low on stock
    items = ActiveProduct.objects.all()
    outOfStock=[]
    lowStock=[]
    highStock=[]
    for item in items:
        if item.get_stock() == 0:
            outOfStock.append(item.Product.ProductName)
        elif item.get_stock() <= item.minimumStockQuantity /2:
            lowStock.append(item.Product.ProductName)
        elif item.get_stock() > item.minimumStockQuantity:
            highStock.append(item.Product.ProductName)
#Low Stock Items
    
    return render(request,"grid.html",{"WriteOffs":newA,"WriteOffsBBD":newB,"WriteOffsDamages":newC, "outOfStock":outOfStock[:6], "lowStock":lowStock[:6],"highStock":highStock[:6]})