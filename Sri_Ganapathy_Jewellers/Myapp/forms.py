from django import forms
from django.contrib.auth.models import User
from Myapp import models
from bootstrap_datepicker_plus import DatePickerInput
from datetime import date

ItemType = (
    ("Gold","Gold"),
    ("Silver","Silver"),
    ("Diamond","Diamond"),
    ("Platinum","Platinum"),
)

Nature_choice = (
    ("916","916"),
    ("ordinary","ordinary"),
)

Item_choices =(
    ("nethichuti","nethichuti"),
    ("kammal","kammal"),
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


class BasicInfo(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BasicInfo, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control bord',
        })
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username","password","email")

class AdditionalInfo(forms.ModelForm):
    a= date.today().strftime("%Y-%m-%d")
    DOB = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d',options={
        "maxDate":a
        }))
    
    def __init__(self,*args,**kwargs):
        super(AdditionalInfo,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control bord',
                
            })

    class Meta:
        model = models.ShopHandlersSignUp
        fields = ("ShopHandlers_id","NickName","Sex","DOB","PhoneNumber","Alt_PhoneNumber")

class Customer_signup(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(Customer_signup,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label,
            })

    class Meta:
        model = models.ShopCustomers
        fields = ("Name","PhoneNumber")

class Metal_pricing(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(Metal_pricing,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control Price',
                'placeholder': self.fields[field].label,
            })

    class Meta:
        model = models.MaterialPricing
        fields = ("Gold_Price","Silver_Price","Platinum_Price","Diamond_Price")

class BillingForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(BillingForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control Price',
                'placeholder': self.fields[field].label,
            })

    class Meta:
        model = models.BillingItems
        fields = "__all__"

class ResourceStockForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(ResourceStockForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
    class Meta:
        model = models.Stock
        fields = "__all__"

class ResourceBulkAddForm(forms.ModelForm):
    a= date.today().strftime("%Y-%m-%d")
    date = forms.DateField(widget= DatePickerInput(format='%Y-%m-%d',options={
        "maxDate":a
    }))

    def __init__(self,*args,**kwargs):
        super(ResourceBulkAddForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
    class Meta:
        model = models.StockAdd
        fields = ("Dealer_Name","Metal_Type","Nature","Weight","Amount","date")

class ResourceBulkPayForm(forms.ModelForm):
    a= date.today().strftime("%Y-%m-%d")
    Date_Paid = forms.DateField(widget= DatePickerInput(format='%Y-%m-%d',options={
        "maxDate":a
    }))
    Amount_paid = forms.CharField(max_length=16)
    def __init__(self,*args,**kwargs):
        super(ResourceBulkPayForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
    
    class Meta:
        model = models.StockPaid
        fields = ("Date_Paid","Payment_Mode","Amount_paid")

class PointsUpdateForm(forms.ModelForm):
    Phone_Number = forms.CharField(max_length=16,required=True)

    def __init__(self,*args,**kwargs):
        super(PointsUpdateForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
    class Meta:
        model = models.PointTable
        fields = ("Phone_Number","Item_Type","Weight")

class RepairForm(forms.Form):

    a= date.today().strftime("%Y-%m-%d")
    Delivery_Estimated = forms.DateField(widget= DatePickerInput(format='%Y-%m-%d',options={
        "minDate":a
    }))

    Description = forms.CharField(widget=forms.Textarea(attrs={'cols:':2,'rows':7}),required = True)
    Metal_type = forms.CharField(widget = forms.Select(choices=ItemType)) 
    Item_type = forms.CharField(widget = forms.Select(choices=Item_choices))
    Price = forms.CharField(max_length=8)

    def __init__(self,*args,**kwargs):
        super(RepairForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {
                'class':'form-control',
                })

class RepairInitalForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(RepairInitalForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {
                'class':'form-control',
                })

    class Meta():
        model = models.Repair
        fields = ("Name","Phone_Number")

class ChitBillNew(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(ChitBillNew,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {
                'class':'form-control',
                })
    Phone_Number = forms.CharField(min_length=10,max_length=13)
    name = forms.CharField(max_length=20)

    class Meta:
        model = models.ChitBill
        fields = ("Phone_Number","name","Address","Type_Of_Scheme","Number_Of_Months_or_Weeks","Amount")

class SearchForm(forms.Form):
    Name = forms.CharField(max_length=32)
    def __init__(self,*args,**kwargs):
        super(SearchForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {
                'class':'form-control',
                })

class PaymentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(PaymentForm,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {
                'class':'form-control',
                })
    class Meta:
        model = models.BillingPayment
        fields = ("Card","Card_Holder","Card_Amount","Online_Transfer_UPI","Online_Amount","Chit_No",
                    "Chit_Amount","Cash","GST_Tax","Balance","Total","Discount","Advance")

class OldJewel(forms.Form):
    Item_Type = forms.CharField(widget = forms.Select(choices=ItemType))
    Nature = forms.CharField(widget = forms.Select(choices=Nature_choice))
    weight_in_grams = forms.CharField(min_length=1)
    Total = forms.CharField(min_length=1)
    def __init__(self,*args,**kwargs):
        super(OldJewel,self).__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update(
                {
                'class':'form-control',
                })
