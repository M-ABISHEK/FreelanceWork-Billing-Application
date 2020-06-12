from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from datetime import date
from django.urls import reverse
# Create your models here.
Sex_choices = (
    ("Male","Male"),
    ("Female","Female"),
    ("Others","Others"),
)
Item_Type = (
    ("Gold","Gold"),
    ("Silver","Silver"),
    ("Diamond","Diamond"),
    ("Platinum","Platinum"),
)
Payment_choices=(
    ("Cash","Cash"),
    ("Card","Card"),
    ("Online","Online"),
    ("Cheque","Cheque"),
)

Item_choices =(
    ("nethichuti","nethichuti"),
    ("Earring","Earring"),
    ("chain","chain"),
    ("Necklace","Necklace"),
    ("Aaram","Aaram"),
    ("Ottiyanam","Ottiyanam"),
    ("Ring","Ring"),
    ("Bangles","Bangles"),
    ("Bracelet","Bracelet"),
    ("Kaapu","Kaapu"),
    ("vangi","vangi"),
    ("Anklets","Anklets"),
    ("ArnaKayiru","ArnaKayiru"),
    ("Metti","Metti"),
    ("Mookuthi","Mookuthi"),
)

Weight_choice=(
    ("916","916"),
    ("Ordinary","Ordinary"),
)

Chit_choice=(
    ("Yes","Yes"),
    ("No","No"),
)

Scheme = (
    ("Monthly","Monthly"),
    ("Weekly","Weekly"),
)

class ShopHandlersSignUp(models.Model):
    user = models.OneToOneField(User,on_delete=models.PROTECT)
    ShopHandlers_id = models.CharField(max_length=20 ,default="")
    NickName = models.CharField(max_length=64,default="None")
    Sex = models.CharField(choices=Sex_choices,max_length=32)
    DOB = models.DateField()
    PhoneNumber = models.CharField(max_length=15,unique=True,help_text="Phone Number")
    Alt_PhoneNumber = models.CharField(max_length=15,help_text="Phone Number")
    Shop_Name = models.CharField(max_length=64,default="Sri Ganapathy Jewellers")

    def __str__(self):
        return self.user.username


class ShopCustomers(models.Model):
    Name = models.CharField(max_length=64)
    PhoneNumber = models.CharField(max_length=15,unique=True,help_text="Phone Number")

    def __str__(self):
        return str(self.PhoneNumber)

class BillingItems(models.Model):
    user = models.ForeignKey(ShopCustomers,on_delete=models.PROTECT)
    Bill_No = models.CharField(max_length=1024,default="")
    Item_id = models.CharField(max_length=2048,default="[]",null=True,blank=True)
    Making_Charge = models.CharField(max_length=2048,default="[]",null=True,blank=True)
    Wastage = models.CharField(max_length=2048,default="[]",null=True,blank=True)
    Item_type = models.CharField(max_length=2048,default="[]",null=True,blank=True)
    Date = models.CharField(default = "",max_length=16)
    Total = models.CharField(max_length=2048,default="[]")
    Total_Amount_PreBill = models.CharField(max_length=64,default="0")


    def __str__(self):
        return self.Bill_No

class BillingPayment(models.Model):
    user = models.ForeignKey(BillingItems,on_delete=models.CASCADE,null=True,blank=True)
    Cash = models.CharField(max_length=64,default="0")
    Card = models.CharField(max_length=64,default="xxxx")
    Card_Holder = models.CharField(max_length=64,default="xxxx")
    Card_Amount = models.CharField(max_length=64,default="0")
    Online_Transfer_UPI = models.CharField(max_length=64,default="xxxx")
    Online_Amount = models.CharField(max_length=64,default="0")
    Chit_No = models.CharField(max_length=16,default="0")
    Chit_Amount = models.CharField(max_length=64,default="0")
    GST_Tax = models.CharField(max_length=32,default="0.0",null=True,blank=True)
    CGST_Tax = models.CharField(max_length=32,default="0.0",null=True,blank=True)
    SGST_Tax = models.CharField(max_length=32,default="0.0",null=True,blank=True)
    IGST_Tax = models.CharField(max_length=32,default="0.0",null=True,blank=True)
    Balance = models.CharField(max_length=32,default="0",null=True,blank=True)
    Discount = models.CharField(max_length=8,default="0",null=True,blank=True)
    Advance = models.CharField(max_length=32,default="0",null=True,blank=True)
    Paid = models.CharField(max_length=16,default=0,null = True, blank= True)
    Total = models.CharField(max_length=64,default="0",null=True,blank=True)

    def __str__(self):
        return str(self.user.Bill_No)

class BalanceCheck_ToBePaid(models.Model):
    BillItem = models.ForeignKey(BillingItems,on_delete = models.CASCADE,null = True, blank = True)
    Date = models.CharField(default="[]",max_length=1024)
    Amount = models.CharField(default="[]",max_length=1024)

    def __str__(self):
        return str(self.BillItem.Bill_No)

class Stock(models.Model):
    Item_id = models.CharField(max_length=32,default="",unique=True)
    Quantity = models.CharField(max_length=32,default="")
    Metal_Type = models.CharField(max_length=16,choices=Item_Type,default="Gold")
    Item_Type = models.CharField(choices=Item_choices,max_length=32,default="Ring")
    Item_Choice = models.CharField(choices=Weight_choice,max_length=32,default="961")
    Weight_In_Grams = models.CharField(max_length=32,default="")

    def __str__(self):
        return self.Item_id

class MaterialPricing(models.Model):
    Date = models.CharField(max_length=20,default="")
    Gold_Price = models.CharField(max_length=32,default="")
    Platinum_Price = models.CharField(max_length=32,default="")
    Silver_Price = models.CharField(max_length=32,default="")
    Diamond_Price = models.CharField(max_length=32,default="")

    def __str__(self):
        return str(self.Date)

class StockAdd(models.Model):
    Stock_No = models.CharField(max_length=512,default="")
    Dealer_Name = models.CharField(max_length=32,default="")
    Metal_Type = models.CharField(choices=Item_Type,max_length=16,default="Gold")
    Nature = models.CharField(choices=Weight_choice,max_length=8,default="916")
    Weight = models.CharField(max_length=128,default="")
    Amount = models.CharField(max_length=32,default="")
    Date = models.DateField(default=date.today().strftime("%Y-%m-%d"))

    def __str__(self):
        return self.Dealer_Name

class StockPaid(models.Model):
    Dealer = models.ForeignKey(StockAdd,on_delete=models.CASCADE,null = True, blank = True)
    Payment_Mode = models.CharField(choices=Payment_choices,max_length=16,default="Cash")
    Payment = models.CharField(max_length=1024,default="[]")
    Amount_Paid = models.CharField(max_length=1024,default="[]")
    Date_Paid = models.CharField(max_length=1024,default="[]")
    TotalBalance = models.CharField(max_length=16,default="0")

    def __str__(self):
        return self.Dealer.Dealer_Name


class PointTable(models.Model):
    Name = models.ForeignKey(ShopCustomers,on_delete = models.PROTECT,null = True, blank = True)
    Weight = models.CharField(max_length=16,default="")
    Item_Type = models.CharField(max_length=16,choices=Item_Type,default="Gold")
    Amount_Earned = models.CharField(max_length=16,default="")
    Points_Earned = models.CharField(max_length=16,default="")

    def __str__(self):
        return self.Name.Name

class Repair(models.Model):
    Bill_No = models.CharField(max_length=32,default="")
    Name = models.CharField(max_length=32,default="")
    Phone_Number = models.CharField(max_length=16,default="")
    Metal_Type = models.CharField(max_length=256,default="[]")
    Item_Type = models.CharField(max_length=256,default="[]")
    Repairing_Reason = models.CharField(max_length=1024,default="[]")
    Amount = models.CharField(max_length=128,default="[]")
    Total_Amount = models.CharField(max_length=32,default="")
    Given_Date = models.CharField(default=str(date.today().strftime("%Y-%m-%d")),max_length=16)
    Delivery_Estimated_Date = models.CharField(default="[]",max_length=128)
    Delivery_Status = models.CharField(max_length=16,default="Not Delivered")
    Delivered_Date = models.CharField(default="",max_length=16)

    def __str__(self):
        return self.Bill_No

class ChitBill(models.Model):
    Chit_No = models.CharField(max_length=16,default="",null = True, blank = True)
    Start_Date = models.DateField(default = date.today().strftime("%Y-%m-%d"))
    End_Date = models.DateField(default = date.today().strftime("%Y-%m-%d"))
    Name = models.ForeignKey(ShopCustomers,on_delete=models.CASCADE,null = True, blank = True)
    Address = models.CharField(max_length=1024,default="")
    Type_Of_Scheme = models.CharField(choices=Scheme,default="Weekly",max_length=32)
    Number_Of_Months_or_Weeks = models.CharField(max_length=16,default="")
    Amount = models.CharField(max_length=16,default="")

    def __str__(self):
        return self.Name.Name

class ChitBillUpdate(models.Model):
    Name = models.ForeignKey(ChitBill,on_delete=models.CASCADE,null = True, blank = True)
    Amount = models.CharField(max_length=2048,default="[]")
    Date = models.CharField(max_length=2048,default="[]")
    Status = models.CharField(max_length=16,default="On Going")

    def __str__(self):
        return self.Name.Name.Name

class Oldjewel(models.Model):
    Bill = models.ForeignKey(BillingItems,null = True,blank = True, on_delete = models.CASCADE)
    Item_Type = models.CharField(choices = Item_Type,default="Gold",max_length=16)
    Nature = models.CharField(choices=Weight_choice,default = "916",max_length=16)
    Item = models.CharField(max_length=2048,default="[]")
    weight_in_grams = models.CharField(max_length=2048,default="[]")
    Total = models.CharField(max_length=2048,default="[]")
    Amount = models.CharField(max_length=16,default="0",null = True,blank = True)

    def __str__(self):
        return self.Bill.Bill_No