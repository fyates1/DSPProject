from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib import messages
from Inventory.models import StockItem, sequence, ActiveProduct,WriteOff
from Inventory.views import managerOnly
from django.db.models import Q
from .forms import BBDForm

@login_required(login_url="/login/")
def removals(request):
    if request.method=="POST":
        item_id = request.POST["item_id"]
        quantity = request.POST["quantity"]

        try:
            item = StockItem.objects.get(id=item_id)
        except StockItem.DoesNotExist:
            messages.error(request, "That item no longer exists")
            return redirect("Freshness:freshness")

        if item.quantity < int(quantity):
            messages.error(request,"You tried writing off more items than exist!")
        else:
            writeoff = WriteOff(item = item, quantity = quantity,reason = request.POST["reason"])
            writeoff.save()
            messages.success(request, "Items Removed")

        return redirect("Freshness:freshness")
    items= StockItem.objects.filter(Q(bestBeforeDate__lte=date.today())).order_by('activeProduct__sequence__position')


    return render(request,'freshness.html',{"items":items})
    

    
@login_required(login_url="/login/")
@managerOnly
def BBDAllocation(request):
    if request.method=="POST":
        id = request.POST["item"]
        item = StockItem.objects.get(pk=id)
        print(item)
        form=BBDForm(request.POST)
        if form.is_valid():
            print(item.bestBeforeDate)
            bbd=form.cleaned_data.get("bestBeforeDate")
            item.bestBeforeDate = bbd
            item.save()
            return redirect("Freshness:BBDAllocation")
    else:
        items= StockItem.objects.filter(Q(bestBeforeDate__isnull=True)).order_by('activeProduct__sequence__position')
        form = BBDForm()

    return render(request,'BBDAllocation.html',{"items":items,"form":form})