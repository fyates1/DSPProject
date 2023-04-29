from django.db import models
import uuid

class Product(models.Model):
    ProductName= models.CharField(max_length=100)
    Brand= models.CharField(max_length=100)
    Price = models.FloatField()
    DiscountPrice=models.FloatField()
    Image_Url= models.CharField(max_length=300)
    Category= models.CharField(max_length=100)
    Barcode = models.CharField(max_length=16)
    EAN = models.CharField(max_length=6)

    def __str__(self):
        return self.ProductName

class ActiveProduct(models.Model):
    Product= models.ForeignKey(Product, on_delete=models.RESTRICT)
    minimumStockQuantity = models.IntegerField(default=0)
    Classes= (("N/A","N/A"),
        ("EXTRA CLASS","Extra Class"),
        ("CLASS 1","Class 1"),
        ("CLASS 2","Class 2"))
    Class = models.CharField(max_length=11,choices=Classes,default="N/A")
    def get_stock(self):
        stock_items = StockItem.objects.filter(activeProduct=self.id)
        total_stock = sum(stock_item.quantity for stock_item in stock_items)
        return total_stock
    def get_sequence(self):
        return sequence.objects.get(product=self)

    def __str__(self):
        return self.Product.ProductName

class sequence(models.Model):
    product = models.OneToOneField(ActiveProduct, on_delete=models.RESTRICT)
    position = models.IntegerField(default=0)


class StockItem(models.Model):
    activeProduct= models.ForeignKey(ActiveProduct, on_delete=models.RESTRICT)
    bestBeforeDate = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(default=1)
    UniqueBarcode = models.TextField(default="1")
    def get_barcode(self):
        code = []
        UniqueBarcode=f"{uuid.uuid4()}"
        return UniqueBarcode
    def save(self,*args,**kwargs):
        self.UniqueBarcode = self.get_barcode()
        super(StockItem,self).save(*args,**kwargs)
    

class WriteOff(models.Model):
    item = models.ForeignKey(StockItem, on_delete=models.RESTRICT)
    quantity = models.IntegerField()
    choices = (("BBD","bbd"),("DAMAGES","Damages"),("OTHER","Other"))
    reason = models.CharField(max_length=10,choices=choices,default="OTHER")
    created_at = models.DateTimeField(auto_now_add=True)
    def getAmmount(self):
        ammount = self.item.activeProduct.Product.Price * self.quantity
        return ammount

    def save(self,*args,**kwargs):
        self.item.quantity -= int(self.quantity)
        self.item.save()
        super(WriteOff,self).save(*args,**kwargs)


                
class Sale(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)




class saleItem(models.Model):
    sale = models.ForeignKey(Sale,on_delete=models.CASCADE)
    product = models.ForeignKey(StockItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


