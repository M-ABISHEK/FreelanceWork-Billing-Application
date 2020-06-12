from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView,UpdateView,DeleteView,View
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse,reverse_lazy
from Myapp import forms,models
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import json,random,os
from datetime import date,datetime,timedelta
from dateutil.relativedelta import relativedelta
from sequences import get_next_value
from Myapp.utils import render_to_pdf
# Create your views here.

@login_required
def DangerAhead(request):
    if request.method == "POST":
        Password = request.POST.get("password")
        if Password == "BotBala":
            models.BillingItems.objects.all().delete()
            models.Stock.objects.all().delete()
            models.StockAdd.objects.all().delete()
            models.PointTable.objects.all().delete()
            models.Repair.objects.all().delete()
            models.ChitBill.objects.all().delete()
            return redirect(reverse('jewel:MP'))
        else:
            return render(request,"Danger/Danger.html",{"error":"Trespassers Are Not Allowed"})
    return render(request,"Danger/Danger.html")

class HomeTemplateView(TemplateView):
    template_name = "FirstApp/Home.html"

class PricingTemplateView(TemplateView):
    template_name = "FirstApp/Pricing.html"

def SignUp(request):
    registered = False
    if request.method == "POST":
        basicform = forms.BasicInfo(request.POST)
        additionalform = forms.AdditionalInfo(request.POST)
        if basicform.is_valid() and additionalform.is_valid():
            user_basic = basicform.save()
            user_basic.set_password(user_basic.password)
            user_basic.save()
            user_additional = additionalform.save(commit=False)
            user_additional.user = user_basic
            user_additional.save()
            registered = True
            return redirect(reverse('login'))
            # return render(request,"FirstApp/LoginPage.html",{'reg':registered})
            # reverse('login')
    else:
        basicform = forms.BasicInfo()
        additionalform = forms.AdditionalInfo()
    return render(request,"FirstApp/SignUpPage.html",{"form":basicform,"form1":additionalform,"reg":registered})

def UserLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('jewel:MP'))
        else:
            return render(request,"FirstApp/LoginPage.html",{"error":"Invalid ID or Password"})    
    else:
        return render(request,"FirstApp/LoginPage.html")

@login_required
def UserLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

# ------------------------------------------------------< ADDITIONAL FEATURES FUNCTIONS >------------------------------------------------------------------

@login_required
def New_Customer_SignUp(request):
    # To Register the New Customer Account in Shop
    if request.method == "POST":
        SignUpForm = forms.Customer_signup(request.POST)
        if SignUpForm.is_valid():
            datas = SignUpForm.save()
            datas.save()
    else:
        SignUpForm = forms.Customer_signup()
    return render(request,"Sales/Sale.html",{"form":SignUpForm})

# ----------------------------------------< To Check the Customer Account registered in the shop >---------------------------------------------------------

@login_required
def SaleTemplate(request):
    if request.method == "POST":
        check = models.ShopCustomers.objects.filter(PhoneNumber=request.POST.get('name'))
        if check:
            return render(request,"Sales/Sale.html",{"found":check,"BillNo":get_next_value()})
        else:
            return render(request,"Sales/Sale.html",{"message":"No account"})
    else:
        return render(request,"Sales/Sale.html")

# ---------------------------------------------< LIST OF ALL BILLS >-------------------------------------------------------------

@login_required
def AllBills(request):
    data = models.BillingPayment.objects.all().order_by("-user__Date")
    return render(request,"Sales/AllBills.html",{'data':data})

@login_required
def AllBillsDetails(request,pk_DN):
    dataobj = get_object_or_404(models.BillingItems,Bill_No = pk_DN)
    Ph = str(dataobj.user.PhoneNumber)
    return redirect(reverse('jewel:SalesBill',kwargs={"pk_ph":Ph,"pk_bn":pk_DN}))

# -------------------------------------------------< CHECKING THE BILL IS ALREADY UPDATED >----------------------------------------------------------------
@login_required
def PreBill(request,pk_ph,pk_bn):
    checking = models.BillingItems.objects.filter(user__PhoneNumber = str(pk_ph),Bill_No=str(pk_bn))
    Stock = models.Stock.objects.all()
    DateT = date.today()
    Payment = models.BillingPayment.objects.filter(user__Bill_No = pk_bn)
    if Payment:
        models.BillingPayment.objects.filter(user__Bill_No = pk_bn).update(GST_Tax = "0",CGST_Tax = "0",IGST_Tax = "0",SGST_Tax = "0",
        Balance = "0",Discount = "0",Paid = "0",Total = "0")
    if checking: 
        pass
    else:
        cust = get_object_or_404(models.ShopCustomers,PhoneNumber=pk_ph)
        models.BillingItems.objects.create(user = cust,Bill_No = str(pk_bn),Date = DateT)
    customer = models.ShopCustomers.objects.filter(PhoneNumber=pk_ph)
    if request.method == "POST":
        itemid = request.POST.get("Item_Id")
        makingcharge = request.POST.get("Making_Charge")
        wastage = request.POST.get("Wastage")
        itemcheck = models.Stock.objects.filter(Item_id = itemid)
        if itemcheck:
            itemobj = get_object_or_404(models.Stock,Item_id = itemid)
            datas = get_object_or_404(models.BillingItems,Bill_No = str(pk_bn),Date = DateT)
            func = Calculators()
            ItemList = func.updatelist(datas.Item_id,itemid)
            MakingChargeList = func.updatelist(datas.Making_Charge,makingcharge)
            WastageList = func.updatelist(datas.Wastage,wastage)
            ItemTypeList = func.updatelist(datas.Item_type,str(itemobj.Item_Type)+" [ "+str(itemobj.Metal_Type)+" ] "+" [ "+str(itemobj.Item_Choice)+" ]")
            Price = func.AmountCalculator(wastage,makingcharge,itemid,str(itemobj.Metal_Type))
            PriceList = func.updatelist(datas.Total,Price)
            OverallPrice = func.PrebillAmount(datas.Total_Amount_PreBill,PriceList)
            print(OverallPrice)
            models.BillingItems.objects.filter(user__PhoneNumber = str(pk_ph),Bill_No=str(pk_bn)).update(
                Item_id = ItemList,Making_Charge = MakingChargeList,Wastage = WastageList,
                Item_type = ItemTypeList,Total = PriceList,Total_Amount_PreBill = OverallPrice
            )
            return render(request,"Sales/Pre_bill.html",
                {"Name":customer,"Date":DateT,"Total":str(OverallPrice),"zippedList":zip(json.loads(ItemList),json.loads(ItemTypeList),
                json.loads(MakingChargeList),json.loads(WastageList),json.loads(PriceList)),"Stock":Stock})
        else:
            obj = get_object_or_404(models.BillingItems,Bill_No = str(pk_bn),Date = DateT)
            zippedList = zip(json.loads(obj.Item_id),json.loads(obj.Item_type),json.loads(obj.Making_Charge),json.loads(obj.Wastage),
                            json.loads(obj.Total))
            return render(request,"Sales/Pre_bill.html",{"Name":customer,"Date":DateT,"zippedList":zippedList,
            "Total":str(obj.Total_Amount_PreBill),"Stock":Stock,"error":"Item ID Mismatch"})
    else:
        obj = get_object_or_404(models.BillingItems,Bill_No = str(pk_bn),Date = DateT)
        zippedList = zip(json.loads(obj.Item_id),json.loads(obj.Item_type),json.loads(obj.Making_Charge),json.loads(obj.Wastage),
                        json.loads(obj.Total))
        return render(request,"Sales/Pre_bill.html",{"Name":customer,"Date":DateT,"zippedList":zippedList,
        "Total":str(obj.Total_Amount_PreBill),"Stock":Stock})

@login_required
def BillGST(request,pk_ph,pk_bn):
    # Online Payment
    Card_Name = request.POST.get('Card')
    Card_Number = request.POST.get("Card_Holder")
    CardAmount = request.POST.get("Card_Amount")
    OnlineUPI = request.POST.get("Online_Transfer_UPI")
    OnlineUPIPayment = request.POST.get("Online_Amount")
    ChitNo = request.POST.get("Chit_No")
    ChitAmount = request.POST.get("Chit_Amount")
    Cash = request.POST.get("Cash")
    Advance = request.POST.get("Advance")
    Balance = request.POST.get("Balance")
    DateT = date.today()
    Name =  models.ShopCustomers.objects.filter(PhoneNumber=pk_ph)
    obj = get_object_or_404(models.BillingItems,Bill_No = str(pk_bn))
    zippedList = zip(json.loads(obj.Item_id),json.loads(obj.Item_type),json.loads(obj.Making_Charge),json.loads(obj.Wastage),
                    json.loads(obj.Total))
    check = models.BillingPayment.objects.filter(user__Bill_No = str(pk_bn))
    if check:
        pass
    else:
        models.BillingPayment.objects.create(user = obj)
    check1 = models.Oldjewel.objects.filter(Bill = obj)
    if check1:
        pass
    else:
        models.Oldjewel.objects.create(Bill = obj)
    exchangeobj = get_object_or_404(models.Oldjewel,Bill = obj)
    exchangezip = zip(json.loads(exchangeobj.Item),json.loads(exchangeobj.weight_in_grams),json.loads(exchangeobj.Total))
    exchange = exchangeobj.Amount
    checkObj = get_object_or_404(models.BillingPayment,user__Bill_No = str(pk_bn))
    AmountPaid = float(checkObj.Paid)+float(checkObj.Balance)
    if request.method == "POST":
        if request.POST.get("weight_in_grams") and request.POST.get("Nature") and request.POST.get("Total") and request.POST.get("Item_Type"):
            cal = Calculators()
            item = request.POST.get("Item_Type")+" [ "+request.POST.get("Nature")+" ] "
            ItemList = cal.updatelist(exchangeobj.Item,item)
            WeightList = cal.updatelist(exchangeobj.weight_in_grams,str(request.POST.get("weight_in_grams")))
            PriceList = cal.updatelist(exchangeobj.Total,str(request.POST.get("Total")))
            Total = cal.Amountcal(PriceList)
            models.Oldjewel.objects.filter(Bill = obj).update(weight_in_grams = WeightList,Item = ItemList,Total = PriceList,Amount = Total)
            oldobj = get_object_or_404(models.BillingItems,Bill_No = str(pk_bn))
            l = json.loads(oldobj.Total)
            T = 0
            for i in l:
                T+= float(i)
            total = float(T) - float(Total)
            models.BillingItems.objects.filter(Bill_No = str(pk_bn)).update(Total_Amount_PreBill = total)
            return redirect(reverse("jewel:PreBillGST",kwargs={"pk_ph":pk_ph,"pk_bn":pk_bn}))
        elif request.POST.get("Discount") and request.POST.get("GST") and request.POST.get("IGST"):
            Total = float(obj.Total_Amount_PreBill)+(float(obj.Total_Amount_PreBill)*float(request.POST.get("GST"))/100)+(float(obj.Total_Amount_PreBill)*float(request.POST.get("IGST"))/100) - float(request.POST.get("Discount"))
            GST = float(obj.Total_Amount_PreBill)*float(request.POST.get("GST"))/100
            models.BillingPayment.objects.filter(user__Bill_No = str(pk_bn)).update(GST_Tax = str(GST),CGST_Tax = str(float(GST)/2),
            SGST_Tax = str(float(GST)/2),Discount = request.POST.get("Discount"),Total = str(float(round(Total))),
            IGST_Tax = float(obj.Total_Amount_PreBill)*float(request.POST.get("IGST"))/100,Paid = "0")
            return redirect(reverse("jewel:PreBillGST",kwargs={"pk_ph":pk_ph,"pk_bn":pk_bn}))
        else:
            form =  forms.PaymentForm(request.POST)
            if form.is_valid():
                if ChitNo != "0":
                    checkChit = models.ChitBill.objects.filter(Chit_No = str(ChitNo))
                    if checkChit:
                        chitobj = get_object_or_404(models.ChitBillUpdate,Name__Chit_No = str(ChitNo))
                        if chitobj.Status  != "On Going":
                            pass
                        else:
                            return render(request,"Sales/PaymentProcess.html",{"Name":Name,"Date":DateT,"zippedList":zippedList,
                             "Total":obj.Total_Amount_PreBill,"form":forms.PaymentForm(request.POST),
                             "ErrorChit":"Chit was not Closed","check":check,"ex":exchange})
                    else:
                        return render(request,"Sales/PaymentProcess.html",{"Name":Name,"Date":DateT,"zippedList":zippedList,
                             "Total":obj.Total_Amount_PreBill,"form":forms.PaymentForm(request.POST),
                             "ErrorChit":"Incorrect Chit Number","check":check,"ex":exchange})
                else:
                    pass
                TaxObj = get_object_or_404(models.BillingPayment,user__Bill_No = str(pk_bn))
                Total = float(TaxObj.Total)
                Paid = float(CardAmount)+float(OnlineUPIPayment)+float(Cash)+float(ChitAmount)+float(Advance)
                if str(Total) == str(Paid+float(Balance)):
                    models.BillingPayment.objects.filter(user__Bill_No = str(pk_bn)).update(Card = Card_Name,Card_Holder = Card_Number,Card_Amount = CardAmount,
                                                        Online_Transfer_UPI = OnlineUPI,Online_Amount = OnlineUPIPayment,
                                                        Chit_No = ChitNo,Chit_Amount = ChitAmount,Cash = Cash,Balance = Balance,
                                                        Paid = float(Paid),Advance = Advance)
                    models.BillingItems.objects.filter(Bill_No = str(pk_bn)).update(Total_Amount_PreBill = Total)
                    return redirect(reverse("jewel:PreBillGST",kwargs={"pk_ph":pk_ph,"pk_bn":pk_bn}))
                else:
                    return render(request,"Sales/PaymentProcess.html",{"Name":Name,"Date":DateT,"zippedList":zippedList,
                             "Total":obj.Total_Amount_PreBill,"form":forms.PaymentForm(request.POST),"oldform":forms.OldJewel(),
                             "ErrorAmount":"Please check Payment","check":check,"Paid":str(AmountPaid),"ex":exchange,"ezip":exchangezip})
    else:
        return render(request,"Sales/PaymentProcess.html",{"Name":Name,"Date":DateT,"zippedList":zippedList,
                        "Total":obj.Total_Amount_PreBill,"form":forms.PaymentForm(),"check":check,"Paid":str(AmountPaid),
                        "oldform":forms.OldJewel(),"ex":exchange,"ezip":exchangezip})

@login_required
def exchangeremove(request,pk_ph,pk_bn,pk_er):
    cal = Calculators()
    obj = get_object_or_404(models.BillingItems,Bill_No = str(pk_bn))
    removeobj = get_object_or_404(models.Oldjewel,Bill = obj)
    rm = json.loads(removeobj.Total)[int(pk_er)]
    ItemRemove = cal.RemoveList(removeobj.Item,pk_er)
    WeightRemove = cal.RemoveList(removeobj.weight_in_grams,pk_er)
    PriceRemove = cal.RemoveList(removeobj.Total,pk_er)
    Price = cal.Amountcal(PriceRemove)
    new_price = float(obj.Total_Amount_PreBill)+float(rm)
    print(ItemRemove,WeightRemove,PriceRemove,Price)
    models.BillingItems.objects.filter(Bill_No = str(pk_bn)).update(Total_Amount_PreBill = new_price)
    models.Oldjewel.objects.filter(Bill = obj).update(Item = ItemRemove,weight_in_grams = WeightRemove,Total = PriceRemove,Amount = Price)
    return redirect(reverse("jewel:PreBillGST",kwargs={"pk_ph":pk_ph,"pk_bn":pk_bn}))

@login_required
def DeleteItem(request,pk_ph,pk_bn,pk):
    DateT = date.today()
    datas = get_object_or_404(models.BillingItems,Bill_No = str(pk_bn),Date = DateT)
    func1 = Calculators()
    idremove = func1.RemoveList(datas.Item_id,int(pk))
    itemtyperemove = func1.RemoveList(datas.Item_type,int(pk))
    makingchargeremove = func1.RemoveList(datas.Making_Charge,int(pk))
    wastageremove = func1.RemoveList(datas.Wastage,int(pk))
    totalremove = func1.RemoveList(datas.Total,int(pk))
    overallprice = func1.Amountcal(totalremove)
    models.BillingItems.objects.filter(user__PhoneNumber = str(pk_ph),Bill_No=str(pk_bn)).update(
                Item_id = idremove,Making_Charge = makingchargeremove,Wastage = wastageremove,
                Item_type = itemtyperemove,Total = totalremove,Total_Amount_PreBill = overallprice
            )
    return redirect(reverse("jewel:PreBill",kwargs={"pk_ph":pk_ph,"pk_bn":pk_bn}))

@login_required
def deletebill(request,pk_ph,pk_bn):
    models.BillingItems.objects.filter(Bill_No = pk_bn).delete()
    return redirect(reverse("jewel:Sale"))

class GenerateSaleBillInvoice(View,LoginRequiredMixin):
    login_url = "/shop/"
    def get(self, request, pk_ph, pk_bn, *args, **kwargs):
        obj = get_object_or_404(models.BillingItems,Bill_No = str(pk_bn))
        exobj = get_object_or_404(models.Oldjewel,Bill = obj)
        Amount = exobj.Amount
        Date = obj.Date
        l = json.loads(obj.Item_id)
        l1 = []
        for i in l:
            a = get_object_or_404(models.Stock,Item_id = str(i)) 
            l1.append(a.Weight_In_Grams)
        zippedList = zip(json.loads(obj.Item_id),json.loads(obj.Item_type),l1,
                    json.loads(obj.Total))
        checkObj = get_object_or_404(models.BillingPayment,user__Bill_No = str(pk_bn))
        CGST = float(checkObj.CGST_Tax)
        SGST = float(checkObj.SGST_Tax)
        IGST = float(checkObj.IGST_Tax)
        Balance = float(checkObj.Balance)
        Discount = float(checkObj.Discount)
        AmountPaid = checkObj.Total
        Payment = models.BillingPayment.objects.filter(user__Bill_No = str(pk_bn))
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(BASE_DIR,"static\logo.jpg")
        data = {
            'today': Date, 
            'customer_name': str(obj.user.Name),
            'Phone_Number': str(obj.user.PhoneNumber),
            'order_id': str(obj.Bill_No),
            'datas':zippedList,
            'CGST':CGST,
            'SGST':SGST,
            'IGST':IGST,
            'Balance':Balance,
            'Discount':Discount,
            'Payment':Payment,
            'Total_Amount':AmountPaid,
            'path': str(path),
            'Tin_No':"GST/-33ALDPS2067H1Z5",
            'Am':float(Amount),
        }
        pdf = render_to_pdf('pdf/SalesBillInvoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
        
#<--------------------- DAY TO DAY METAL PRICING VIEWS ----------------------->

@login_required
def MetalPricing(request):
    data = models.MaterialPricing.objects.filter(Date = date.today().strftime("%d-%m-%Y"))
    if request.method == "POST":
        dataform = forms.Metal_pricing(request.POST)
        if dataform.is_valid():
            datacheck = models.MaterialPricing.objects.filter(Date = date.today().strftime("%d-%m-%Y"))
            if datacheck:
                models.MaterialPricing.objects.filter(Date = date.today().strftime("%d-%m-%Y")).update(
                    Gold_Price = request.POST.get("Gold_Price"),Silver_Price = request.POST.get("Silver_Price"),
                    Platinum_Price = request.POST.get("Platinum_Price"),Diamond_Price = request.POST.get("Diamond_Price")
                )
            else:
                form = dataform.save()
                form.Date = date.today().strftime("%d-%m-%Y")
                form.save()
                return HttpResponseRedirect(reverse("jewel:MP"))
    else:
        dataform = forms.Metal_pricing()
    if not data:
        form1 = {"message" : "No pricings Updated for Today!!",
                 "message1":"First you need to update the Pricings!"}
        return render(request,"MaterialPricing/materialpricing.html",{"form":dataform,"form1":form1})
    else:
        return render(request,"MaterialPricing/materialpricing.html",{"form":dataform,"data":data})

#<--------------------- RESOURCE STOCK VIEWS ----------------------->

@login_required
def ResourcestockUpdate(request):
    Items = models.Stock.objects.all().order_by("Item_id")
    ResForm = forms.ResourceStockForm()
    if request.method == "POST":
        if request.POST.get("search"):
            searchdata = models.Stock.objects.filter(Item_id = request.POST.get("search"))
            return render(request,"ResourceUpdate/ResourceUpdate.html",{"Data":ResForm,"Items":Items,"searchdata":searchdata,"No":len(Items)})
        else:
            Resource = forms.ResourceStockForm(request.POST)
            if Resource.is_valid():
                Resource.save()
                return HttpResponseRedirect(reverse("jewel:resource"))
            else:
                return render(request,"ResourceUpdate/ResourceUpdate.html",{"Data":ResForm,"Items":Items,"error":"Item ID is Already Here..","No":len(Items)})
    else:
        ResForm = forms.ResourceStockForm()
    return render(request,"ResourceUpdate/ResourceUpdate.html",{"Data":ResForm,"Items":Items,"No":len(Items)})

@login_required
def ResourceDetail(request,slug):
    Detail = models.Stock.objects.filter(Item_Type = str(slug))
    return render(request,"ResourceUpdate/ResourceDetail.html",{"Items":Detail})

@login_required
def ResourceBulk(request):
    return render(request,"ResourceUpdate/ResourceBulkUpdate.html")

@login_required
def ResourceBulkAdd(request):
    table = models.StockAdd.objects.all().order_by("Stock_No")
    Today = date.today()
    if request.method == "POST":
        dataform = forms.ResourceBulkAddForm(request.POST)
        if dataform.is_valid():
            data = dataform.save()
            data.Date = request.POST.get("date")
            data.Stock_No = get_next_value(sequence_name= "Stock_No")
            data.save()
            return HttpResponseRedirect(reverse("jewel:resourcebulkAdd"))
    else:
        dataform = forms.ResourceBulkAddForm()
    return render(request,"ResourceUpdate/ResourceBulkUpdate.html",{"formadd":dataform,"table":table,"Today":Today})

@login_required
def ResourceBulkPay(request):
    data_list = models.StockAdd.objects.all().order_by("Dealer_Name")
    model_list = models.StockPaid.objects.all().order_by("-Date_Paid")
    return render(request,"ResourceUpdate/ResourceBulkUpdate.html",
                {"datalist":data_list,"modellist":model_list})

@login_required
def ResourceBulkPayPk(request,pk_payn):
    dataid = models.StockAdd.objects.filter(id = pk_payn)
    dataid_object = get_object_or_404(models.StockAdd,id = pk_payn)
    check = models.StockPaid.objects.filter(Dealer = dataid_object)
    if check:
        pass
    else:
        models.StockPaid.objects.create(Dealer = dataid_object,TotalBalance = dataid_object.Amount)
    dataobj = get_object_or_404(models.StockPaid,Dealer = dataid_object)
    zippedlist = zip(json.loads(dataobj.Payment),json.loads(dataobj.Amount_Paid),json.loads(dataobj.Date_Paid))
    if request.method == "POST":
        Payform = forms.ResourceBulkPayForm(request.POST)
        if Payform.is_valid():
            obj = get_object_or_404(models.StockPaid,Dealer = dataid_object)
            cal = Calculators()
            if float(obj.TotalBalance) >= float(request.POST.get("Amount_paid")) and float(request.POST.get("Amount_paid")) != 0.0:
                PaymentChoiceList = cal.updatelist(obj.Payment,request.POST.get("Payment_Mode"))
                AmountPaidList = cal.updatelist(obj.Amount_Paid,request.POST.get("Amount_paid"))
                DatePaidList = cal.updatelist(obj.Date_Paid,request.POST.get("Date_Paid"))
                bal = int(obj.TotalBalance)-int(request.POST.get("Amount_paid"))
                models.StockPaid.objects.filter(Dealer = dataid_object).update(
                    Payment = PaymentChoiceList,Amount_Paid = AmountPaidList,
                    Date_Paid = DatePaidList,TotalBalance = str(bal)
                )
                return redirect(reverse("jewel:resourcebulkPayPk",kwargs={"pk_payn":pk_payn}))
            else:
                Payform = forms.ResourceBulkPayForm(request.POST)
                return render(request,"ResourceUpdate/ResourceBulkPay.html",{"Payform":Payform,"dataid":dataid,"paid_list":check,"zippedlist":zippedlist,
                    "TB":dataobj.TotalBalance,"error":"Check Payment"})
    else:
        Payform = forms.ResourceBulkPayForm()
        return render(request,"ResourceUpdate/ResourceBulkPay.html",{"Payform":Payform,"dataid":dataid,"paid_list":check,"zippedlist":zippedlist,
                    "TB":dataobj.TotalBalance,"Today":str(date.today())})

@login_required
def StockDeleteView(request,pk_d):
    models.Stock.objects.filter(pk=pk_d).delete()
    return HttpResponseRedirect(reverse("jewel:resource"))

@login_required
def ResourceBulkPayDelete(request,pk_payn,pk_pd):
    dataid_object = get_object_or_404(models.StockAdd,id = pk_payn)
    dataobj = get_object_or_404(models.StockPaid,Dealer = dataid_object)
    cal = Calculators()
    PaymentRemove = cal.RemoveList(dataobj.Payment,str(pk_pd))
    AmountRemove = cal.RemoveList(dataobj.Amount_Paid,str(pk_pd))
    DateRemove = cal.RemoveList(dataobj.Date_Paid,str(pk_pd))
    Totalbal = int(json.loads(dataobj.Amount_Paid)[int(pk_pd)])+int(dataobj.TotalBalance)
    models.StockPaid.objects.filter(Dealer = dataid_object).update(
        Payment = PaymentRemove,Amount_Paid = AmountRemove,Date_Paid = DateRemove,TotalBalance = str(Totalbal))
    return redirect(reverse("jewel:resourcebulkPayPk",kwargs={"pk_payn":pk_payn}))

@login_required
def ResourceBulkAddDelete(request,pk_ad):
    models.StockAdd.objects.filter(pk = pk_ad).delete()
    return HttpResponseRedirect(reverse("jewel:resourcebulkAdd"))

@login_required
def TotalSummaryStock(request):
    Gold = models.StockAdd.objects.filter(Metal_Type = "Gold")
    Gold1 = models.Stock.objects.filter(Metal_Type = "Gold")
    Silver = models.StockAdd.objects.filter(Metal_Type = "Silver")
    Silver1 = models.Stock.objects.filter(Metal_Type = "Silver")
    Platinum = models.StockAdd.objects.filter(Metal_Type = "Platinum")
    Platinum1 = models.Stock.objects.filter(Metal_Type = "Platinum")
    Diamond = models.StockAdd.objects.filter(Metal_Type = "Diamond")
    Diamond1 = models.Stock.objects.filter(Metal_Type = "Diamond")
    cal = Calculators()
    TGold = cal.TotalStock(Gold,Gold1)
    TSilver = cal.TotalStock(Silver,Silver1)
    TPlatinum = cal.TotalStock(Platinum,Platinum1)
    TDiamond = cal.TotalStock(Diamond,Diamond1)
    return render(request,"ResourceUpdate/StockSummary.html",{"Gold":TGold,"Silver":TSilver,"Platinum":TPlatinum,"Diamond":TDiamond})

#<--------------------- POINTS UPDATE VIEWS ----------------------->

@login_required
def PointsUpdate(request):
    Total_Points = models.PointTable.objects.all()
    if request.method  == "POST":
        if request.POST.get('Search'):
            Search = request.POST.get('Search')
            checkpoint = models.PointTable.objects.filter(Name__PhoneNumber = Search)
            if checkpoint:
                form = forms.PointsUpdateForm()
                return render(request,"PointsUpdate/PointsUpdate.html",{"form":form,"Pointtable":Total_Points,"result":checkpoint})
            else:
                form = forms.PointsUpdateForm()
                return render(request,"PointsUpdate/PointsUpdate.html",{"form":form,"Pointtable":Total_Points,"errors":"No User Found"})
        else:
            form = forms.PointsUpdateForm(request.POST)
            if form.is_valid():
                check = models.ShopCustomers.objects.filter(PhoneNumber = request.POST.get("Phone_Number"))
                if check:
                    Weight = request.POST.get("Weight")
                    Item_Type = request.POST.get("Item_Type")
                    Ph_No = request.POST.get("Phone_Number")
                    Pointfinder = Calculators()
                    Points = Pointfinder.PointsMetal(Item_Type,Weight) # function to find amount for points earned
                    user_check = models.PointTable.objects.filter(Name__PhoneNumber = Ph_No)
                    if user_check:
                        data_update = get_object_or_404(models.PointTable,Name__PhoneNumber = Ph_No)
                        Point = float(data_update.Points_Earned)+float(Points[0])
                        Amount = float(data_update.Amount_Earned)+float(Points[1])
                        models.PointTable.objects.filter(Name__PhoneNumber = Ph_No).update(Points_Earned = str(Point),Amount_Earned = str(Amount))
                    else:
                        Customer_Name = get_object_or_404(models.ShopCustomers,PhoneNumber = Ph_No)
                        Pointform = form.save()
                        Pointform.Name = Customer_Name
                        Pointform.Weight = Weight
                        Pointform.Points_Earned = str(Points[0])
                        Pointform.Amount_Earned = str(Points[1])
                        Pointform.save()
                    return HttpResponseRedirect(reverse('jewel:PointsUpdate'))
                else:
                    form = forms.PointsUpdateForm()
                    return render(request,"PointsUpdate/PointsUpdate.html",
                    {"form":form,"error":"No Accounts Registered with this Phone Number","Pointtable":Total_Points})
    else:
        form = forms.PointsUpdateForm()
    return render(request,"PointsUpdate/PointsUpdate.html",{"form":form,"Pointtable":Total_Points})

#<--------------------- REPAIR VIEWS ----------------------->
@login_required
def RepairInitial(request):
    data = models.Repair.objects.all()
    if request.method == "POST":
        form = forms.RepairInitalForm(request.POST)
        if form.is_valid():
            dataNo = get_next_value(sequence_name="Repair_Bill_No")
            dataform = form.save()
            dataform.Bill_No = str(dataNo)
            dataform.save()
            data = dataNo
            return render(request,"Repair/RepairNew.html",{"datalink":data})
    else:
        form = forms.RepairInitalForm()
    return render(request,"Repair/RepairNew.html",{"form":form,"data":data})

@login_required
def RepairView(request,pk_No):
    data = models.Repair.objects.filter(Bill_No = str(pk_No))
    obj = get_object_or_404(models.Repair,Bill_No = str(pk_No))
    form = forms.RepairForm()
    if request.method == "POST":
        dataobj = get_object_or_404(models.Repair,Bill_No = str(pk_No))
        Metal = request.POST.get("Metal_type")
        Item = request.POST.get("Item_type")
        Description = request.POST.get("Description")
        Delivery_date= request.POST.get("Delivery_Estimated")
        Price = request.POST.get("Price")
        cal = Calculators()
        Metallist = cal.updatelist(dataobj.Metal_Type,str(Metal))
        Itemlist = cal.updatelist(dataobj.Item_Type,str(Item))
        Descriptionlist = cal.updatelist(dataobj.Repairing_Reason,str(Description))
        Deliverydateist = cal.updatelist(dataobj.Delivery_Estimated_Date,str(Delivery_date))
        Pricelist = cal.updatelist(dataobj.Amount,str(Price))
        AmountCal = cal.Amountcal(Pricelist)
        models.Repair.objects.filter(Bill_No = str(pk_No)).update(
            Metal_Type = str(Metallist),Item_Type = str(Itemlist),Repairing_Reason = str(Descriptionlist),
            Delivery_Estimated_Date = str(Deliverydateist),Amount = str(Pricelist),Total_Amount = str(AmountCal),Delivery_Status = "Not Delivered")
        datas = zip(json.loads(Metallist),json.loads(Itemlist),json.loads(Descriptionlist),json.loads(Deliverydateist),json.loads(Pricelist))
        return render(request,"Repair/Repair.html",{"form":form,"datas":datas,"data":data})
    else:
        form = forms.RepairForm()
    zipdata = zip(json.loads(obj.Metal_Type),json.loads(obj.Item_Type),json.loads(obj.Repairing_Reason),
                  json.loads(obj.Delivery_Estimated_Date),json.loads(obj.Amount))
    return render(request,"Repair/Repair.html",{"form":form,"data":data,"datas":zipdata})

@login_required
def RepairItemRemove(request,pk_No,pk_RIR):
    data = get_object_or_404(models.Repair,Bill_No = str(pk_No))
    amount = models.Repair.objects.filter(Bill_No = str(pk_No))
    cal = Calculators()
    Metal_Remove = cal.RemoveList(data.Metal_Type,pk_RIR)
    Item_Remove = cal.RemoveList(data.Item_Type,pk_RIR)
    Description_Remove = cal.RemoveList(data.Repairing_Reason,pk_RIR)
    Delivery_Remove = cal.RemoveList(data.Delivery_Estimated_Date,pk_RIR)
    Price_Remove = cal.RemoveList(data.Amount,pk_RIR)
    Amountlist = cal.Amountcal(Price_Remove)
    models.Repair.objects.filter(Bill_No = str(pk_No)).update(
            Metal_Type = str(Metal_Remove),Item_Type = str(Item_Remove),Repairing_Reason = str(Description_Remove),
            Delivery_Estimated_Date = str(Delivery_Remove),Amount = str(Price_Remove),Total_Amount = str(Amountlist),Delivery_Status = "Not Delivered")
    return redirect(reverse("jewel:RepairView",kwargs={"pk_No":int(pk_No)}))

@login_required
def RepairDelete(request,pk_Nod,pk_No):
    models.Repair.objects.filter(id = pk_Nod).delete()
    return HttpResponseRedirect(reverse("jewel:Repair"))

class GeneratePdf(View,LoginRequiredMixin):
    login_url = "/shop/"
    def get(self, request, pk_No, *args, **kwargs):
        details = get_object_or_404(models.Repair,Bill_No = str(pk_No))
        datas = zip(json.loads(details.Metal_Type),json.loads(details.Item_Type),json.loads(details.Repairing_Reason),
                    json.loads(details.Delivery_Estimated_Date),json.loads(details.Amount))
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(BASE_DIR,"static\logo.jpg")
        data = {
            'today': date.today(), 
            'customer_name': str(details.Name),
            'Phone_Number': str(details.Phone_Number),
            'order_id': str(details.Bill_No),
            'datas':datas,
            'Total_Amount':details.Total_Amount,
            'path': str(path),
        }
        pdf = render_to_pdf('pdf/Repairinvoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

@login_required
def RepairAck(request,pk_Dno):
    data = get_object_or_404(models.Repair,id = pk_Dno)
    zippedlist = zip(json.loads(data.Metal_Type),json.loads(data.Item_Type),json.loads(data.Repairing_Reason),
                     json.loads(data.Delivery_Estimated_Date),json.loads(data.Amount))
    return render(request,"Repair/RepairDetail.html",{"ZippedList":zippedlist,"data":data})

@login_required
def RepairDelivery(request,pk_Dno):
    models.Repair.objects.filter(id = pk_Dno).update(Delivery_Status = "Delivered",Delivered_Date = date.today())
    return redirect(reverse("jewel:Repair"))

#<--------------------- CHITBILL VIEWS ----------------------->

@login_required
def ChitBillOptions(request):
    return render(request,"ChitBill/ChitBillOptions.html")

@login_required
def ChitBillNew(request):
    if request.method == "POST":
        form = forms.ChitBillNew(request.POST)
        if form.is_valid():
            name = request.POST.get("name")
            Phone_Number = request.POST.get("Phone_Number")
            check = models.ShopCustomers.objects.filter(PhoneNumber = Phone_Number)
            if check:
                pass
            else:
                models.ShopCustomers.objects.create(Name = name.lower(),PhoneNumber = Phone_Number)
            data = get_object_or_404(models.ShopCustomers,PhoneNumber = Phone_Number)
            CHITNO = get_next_value(sequence_name="ChitNo")
            dataform = form.save()
            dataform.Name = data
            dataform.Chit_No = CHITNO
            dataform.Start_Date = datetime.now().strftime("%Y-%m-%d")
            if request.POST.get("Type_Of_Scheme") == "Weekly":
                days = int(request.POST.get("Number_Of_Months_or_Weeks"))
                dates = datetime.now()+timedelta(weeks=days)
            else:
                days = int(request.POST.get("Number_Of_Months_or_Weeks"))
                dates = datetime.today()+ relativedelta(months=days)
            dataform.End_Date = dates.strftime("%Y-%m-%d")
            dataform.save()
            dataaftereg = get_object_or_404(models.ChitBill,Chit_No = CHITNO)
            models.ChitBillUpdate.objects.create(Name = dataaftereg)
            return HttpResponseRedirect(reverse("jewel:ChitBillUpdate"))
    else:
        form = forms.ChitBillNew()
    return render(request,"ChitBill/ChitBillNew.html",{"form":form})

@login_required
def ChitBillUpdate(request):
    if request.method =="POST":
        if request.POST.get("Phonenumber"):
            data = models.ChitBill.objects.filter(Name__PhoneNumber = request.POST.get("Phonenumber"))
            if data:
                return render(request,"ChitBill/ChitBillUpdate.html",{"form1":forms.SearchForm(),"data":data})
            else:
                return render(request,"ChitBill/ChitBillUpdate.html",{"form1":forms.SearchForm(),"error":"Incorrect Phone Number"})
        elif request.POST.get("chitno") and request.POST.get("Amount"):
            chitno = request.POST.get("chitno")
            check = models.ChitBillUpdate.objects.filter(Name__Chit_No = chitno,Status = "On Going")
            if check:
                foreigndata = get_object_or_404(models.ChitBill,Chit_No = chitno)
                listconv = get_object_or_404(models.ChitBillUpdate,Name__Chit_No = chitno)
                if listconv.Status == "On Going":
                    cal = Calculators()
                    a = cal.updatelist(listconv.Date,datetime.now().strftime("%Y-%m-%d, %H:%M"))
                    b = cal.updatelist(listconv.Amount,request.POST.get("Amount"))
                    zippedList = zip(json.loads(a),json.loads(b))
                    models.ChitBillUpdate.objects.filter(Name = foreigndata).update(Amount = str(b),Date = str(a))    
                    return render(request,"ChitBill/ChitBillUpdate.html",{"form1":forms.SearchForm(),"check":check,"ziplist":zippedList})
                else:
                    zippedList = zip(json.loads(listconv.Date),json.loads(listconv.Amount))
                    return render(request,"ChitBill/ChitBillUpdate.html",{"form1":forms.SearchForm(),"check":check,
                                "ziplist":zippedList})

            else:
                return render(request,"ChitBill/ChitBillUpdate.html",{"form1":forms.SearchForm(),"error":"Incorrect Chit Number or Chit was Closed"})
    else:
        return render(request,"ChitBill/ChitBillUpdate.html",{"form1":forms.SearchForm()})

@login_required
def ChitBillUpdateid(request,pk_ChitBillID):
    if request.method == "POST":
        if request.POST.get("Phonenumber"):
            data = models.ChitBill.objects.filter(Name__PhoneNumber = request.POST.get("Phonenumber"))
            if data:
                return render(request,"ChitBill/ChitBillUpdate.html",{"form1":forms.SearchForm(),"data":data})
            else:
                return render(request,"ChitBill/ChitBillUpdate.html",{"form1":forms.SearchForm(),"error":"Incorrect Phone Number"})
        elif request.POST.get("chitno") and request.POST.get("Amount"):
            chitno = request.POST.get("chitno")
            check = models.ChitBillUpdate.objects.filter(Name__Chit_No = chitno)
            if check:
                foreigndata = get_object_or_404(models.ChitBill,Chit_No = chitno)
                listconv = get_object_or_404(models.ChitBillUpdate,Name__Chit_No = chitno)
                if listconv.Status == "On Going":
                    cal = Calculators()
                    a = cal.updatelist(listconv.Date,datetime.now().strftime("%Y-%m-%d, %H:%M"))
                    b = cal.updatelist(listconv.Amount,request.POST.get("Amount"))
                    zippedList = zip(json.loads(a),json.loads(b))
                    models.ChitBillUpdate.objects.filter(Name = foreigndata).update(Amount = str(b),Date = str(a))    
                    return render(request,"ChitBill/ChitBillUpdate.html",{"check":check,"ziplist":zippedList})
                else:
                    zippedList = zip(json.loads(listconv.Date),json.loads(listconv.Amount))
                    return render(request,"ChitBill/ChitBillUpdate.html",{"check":check,
                                "ziplist":zippedList})
            else:
                return render(request,"ChitBill/ChitBillUpdate.html",{"error":"Incorrect Chit Number"})
    else:
        data = get_object_or_404(models.ChitBill,id=pk_ChitBillID)
        datacheck =  models.ChitBillUpdate.objects.filter(Name__Chit_No = data.Chit_No)
        zipdata = get_object_or_404(models.ChitBillUpdate,Name__Chit_No = data.Chit_No)
        zippedList = zip(json.loads(zipdata.Date),json.loads(zipdata.Amount))
        return render(request,"ChitBill/ChitBillUpdate.html",{"check":datacheck,"ziplist":zippedList})

@login_required
def ChitClose(request,pk_ChitBillID):
    models.ChitBillUpdate.objects.filter(Name__id = pk_ChitBillID).update(Status = "Closed")
    return redirect(reverse('jewel:ChitBillUpdateid',kwargs={"pk_ChitBillID":pk_ChitBillID}))

# <---------------------------------- Balance Check ---------------------------------->

@login_required
def BalanceCheck(request):
    To_Be_Paid = models.BillingPayment.objects.all()
    To_Pay = models.StockPaid.objects.all()
    return render(request,"BalanceCheck/balance.html",{"d1":To_Be_Paid,"d2":To_Pay})

@login_required
def BalanceToBePaid(request,pk_ToBepaid):
    check = models.BalanceCheck_ToBePaid.objects.filter(BillItem__Bill_No = pk_ToBepaid)
    if check:
        pass
    else:
        models.BalanceCheck_ToBePaid.objects.create(BillItem = get_object_or_404(models.BillingItems,Bill_No = pk_ToBepaid))
    data = models.BillingPayment.objects.filter(user__Bill_No = pk_ToBepaid)
    obj = get_object_or_404(models.BillingPayment,user__Bill_No = pk_ToBepaid)
    zippedlist = zip(json.loads(obj.user.Item_id),json.loads(obj.user.Item_type),json.loads(obj.user.Making_Charge),
                     json.loads(obj.user.Wastage),json.loads(obj.user.Total))
    datacheck = get_object_or_404(models.BalanceCheck_ToBePaid,BillItem__Bill_No = pk_ToBepaid)
    checkzip = zip(json.loads(datacheck.Date),json.loads(datacheck.Amount))
    if request.method == "POST":
        Balance = request.POST.get("Balance")
        obj = get_object_or_404(models.BillingPayment,user__Bill_No = pk_ToBepaid)
        dataobj = get_object_or_404(models.BillingItems,Bill_No = pk_ToBepaid)
        Billobj = get_object_or_404(models.BalanceCheck_ToBePaid,BillItem = dataobj)
        if float(obj.Balance) >= float(Balance) and int(Balance) != 0:
            Balance_Paid = float(obj.Balance)-float(Balance)
            Paid = float(obj.Paid)+float(Balance)
            models.BillingPayment.objects.filter(user__Bill_No = pk_ToBepaid).update(Balance = str(int(Balance_Paid)),Paid = Paid)
            cal = Calculators()
            Amountlist = cal.updatelist(Billobj.Amount,Balance)
            Datelist = cal.updatelist(Billobj.Date,str(date.today()))
            models.BalanceCheck_ToBePaid.objects.filter(BillItem__Bill_No = pk_ToBepaid).update(Amount = Amountlist,Date = Datelist)
            return redirect(reverse("jewel:BalanceToBePaid",kwargs={"pk_ToBepaid":pk_ToBepaid}))
        else:
            error = "Check The Amount"
            return render(request,"BalanceCheck/balancedetail.html",{"d1":data,"error":error,"data":zippedlist,"zip":checkzip})
    else:
        pass
    return render(request,"BalanceCheck/balancedetail.html",{"d1":data,"data":zippedlist,"zip":checkzip})
                
@login_required
def BalanceToBePaidDelete(request,pk_ToBepaid,pk_ToBepaidD):    
    cal = Calculators()
    obj = get_object_or_404(models.BalanceCheck_ToBePaid,BillItem__Bill_No = pk_ToBepaid)
    alterobj = get_object_or_404(models.BillingPayment,user__Bill_No = pk_ToBepaid)
    data = json.loads(obj.Amount)[int(pk_ToBepaidD)]
    paid = float(alterobj.Paid)-float(data)
    Amount = float(data)+float(json.loads(alterobj.Balance))
    DateRemoveList = cal.RemoveList(obj.Date,pk_ToBepaidD)
    AmountRemoveList = cal.RemoveList(obj.Amount,pk_ToBepaidD)
    models.BalanceCheck_ToBePaid.objects.filter(BillItem__Bill_No = pk_ToBepaid).update(Date = DateRemoveList,Amount = AmountRemoveList)
    models.BillingPayment.objects.filter(user__Bill_No = pk_ToBepaid).update(Balance = str(int(Amount)),Paid = str(paid))
    return redirect(reverse("jewel:BalanceToBePaid",kwargs={"pk_ToBepaid":pk_ToBepaid}))

@login_required
def BalanceStockToPay(request,pk_Topay):
    return redirect(reverse("jewel:resourcebulkPayPk",kwargs={"pk_payn":pk_Topay}))
# -----------------------------------------------< ADDITIONAL FUNCTIONS FOR CALCULATIONS >-----------------------------------------------------
class Calculators():

    def AmountCalculator(self,wastage,makingcharge,itemid,metal):
        Total_Amount=0
        Item_Price = get_object_or_404(models.Stock,Item_id=itemid)
        Grams = float(Item_Price.Weight_In_Grams)
        PricePerGram = float(Calculators.Metal(self,metal))
        Total_Amount = (Grams*PricePerGram)+(int(wastage)+int(makingcharge))
        return Total_Amount

    def Metal(self,metaltype):
        MetalTypeFinder = get_object_or_404(models.MaterialPricing,Date = date.today().strftime("%d-%m-%Y"))
        if metaltype == "Gold":
            return MetalTypeFinder.Gold_Price
        elif metaltype == "Silver":
            return MetalTypeFinder.Silver_Price
        elif metaltype == "Platinum":
            return MetalTypeFinder.Platinum_Price
        elif metaltype == "Diamond":
            return MetalTypeFinder.Diamond_Price

    def PointsMetal(self,Item_Type,Weight):
        if Item_Type == "Gold":
            l=[]
            data = float(Weight)*100
            Amount = float(data*0.10)
            l.append(data)
            l.append(Amount)
            return l
        elif Item_Type == "Silver":
            l=[]
            data = float(Weight)*1
            Amount = float(data*0.01)
            l.append(data)
            l.append(Amount)
            return l

    def updatelist(self,datalist,inputdata):
        e = json.loads(str(datalist))
        e.append(inputdata)
        m = json.dumps(e)
        return m

    def RemoveList(self,datalist,pk):
        e = json.loads(str(datalist))
        e.remove(e[int(pk)])
        m = json.dumps(e)
        return m

    def Amountcal(self,amountlist):
        am = 0
        g = json.loads(str(amountlist))
        for i in g:
            am+=float(i)
        return am 

    def PrebillAmount(self,datas,amountlist):
        am = 0
        g = json.loads(str(amountlist))
        for i in g:
            am+=float(i)
        return round(am)    
    
    def TotalStock(self,datalist,datalist1):
        Metal = 0
        for i in datalist:
            Metal += float(i.Weight)
        for j in datalist1:
            Metal += float(j.Weight_In_Grams)
        return Metal
        