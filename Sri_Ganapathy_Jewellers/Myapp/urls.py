from django.conf.urls import url
from Myapp import views

app_name = "jewel"

urlpatterns=[
    url(r"^New_register/$",views.New_Customer_SignUp,name="customer_register"),
    url(r"^MetalPricingTodayUpdate/$",views.MetalPricing,name="MP"),

    url(r'^BalanceCheck/$',views.BalanceCheck,name="Balance"),
    url(r'^BalanceCheck/(?P<pk_ToBepaid>\d+)/To_Be_Paid/$',views.BalanceToBePaid,name="BalanceToBePaid"),
    url(r'^BalanceCheck/(?P<pk_ToBepaid>\d+)/To_Be_Paid/(?P<pk_ToBepaidD>\d+)/$',views.BalanceToBePaidDelete,name="BalanceToBePaidDelete"),
    url(r'^BalanceCheck/(?P<pk_Topay>\d+)/ToPay/$',views.BalanceStockToPay,name="BalancePay"),

    url(r"^Account/$",views.SaleTemplate,name="Sale"),
    url(r"^Account/AllBills/$",views.AllBills,name="SaleBills"),
    url(r"^Account/AllBills/(?P<pk_DN>\d+)/$",views.AllBillsDetails,name="SaleBillsDetail"),
    url(r'^Account/(?P<pk_ph>\d+)/(?P<pk_bn>\d+)/$',views.PreBill,name="PreBill"),
    url(r'^Account/(?P<pk_ph>\d+)/(?P<pk_bn>\d+)/Delete/$',views.deletebill,name="deleteBill"),
    url(r'^Account/(?P<pk_ph>\d+)/(?P<pk_bn>\d+)/Tax&Discount/$',views.BillGST,name="PreBillGST"),
    url(r'^Account/(?P<pk_ph>\d+)/(?P<pk_bn>\d+)/Tax&Discount/(?P<pk_er>\d+)/$',views.exchangeremove,name="exchangeremove"),
    url(r'^Account/(?P<pk_ph>\d+)/(?P<pk_bn>\d+)/Tax&Discount/SalesBill/$',views.GenerateSaleBillInvoice.as_view(),name="SalesBill"),
    url(r'^Account/(?P<pk_ph>\d+)/(?P<pk_bn>\d+)/(?P<pk>\d+)/$',views.DeleteItem,name="DeleteItem"),

    url(r'^Resources/$',views.ResourcestockUpdate,name="resource"),
    url(r'^Resources/(?P<slug>[\w-]+)/$',views.ResourceDetail,name="resourcedetail"),
    url(r'^Resources/bulk/$',views.ResourceBulk,name="resourcebulk"),
    url(r'^Resources/bulk/Add/$',views.ResourceBulkAdd,name="resourcebulkAdd"),
    url(r'^Resources/bulk/Add/(?P<pk_ad>\d+)/$',views.ResourceBulkAddDelete,name="resourcebulkAddPk"),
    url(r'^Resources/bulk/Pay/$',views.ResourceBulkPay,name="resourcebulkPay"),
    url(r'^Resources/bulk/Pay/(?P<pk_payn>\d+)/$',views.ResourceBulkPayPk,name="resourcebulkPayPk"),
    url(r'^Resources/bulk/Pay/(?P<pk_payn>\d+)/(?P<pk_pd>\d+)/$',views.ResourceBulkPayDelete,name="resourcebulpaydelete"),
    url(r'^Resources/(?P<pk_d>\d+)/$',views.StockDeleteView,name="StockDelete"),
    url(r'^TotalStockSummary/$',views.TotalSummaryStock,name="Summary"),

    url(r'^PointsUpdate/$',views.PointsUpdate,name="PointsUpdate"),

    url(r'^Repair/$',views.RepairInitial,name="Repair"),
    url(r'^Repair/Details/(?P<pk_Dno>\d+)/$',views.RepairAck,name="RepairDetail"),
    url(r'^Repair/Details/(?P<pk_Dno>\d+)/ACK/$',views.RepairDelivery,name="RepairDetailAck"),
    url(r'^Repair/(?P<pk_No>\d+)/$',views.RepairView,name="RepairView"),
    url(r'^Repair/(?P<pk_No>\d+)/PDF/$',views.GeneratePdf.as_view(),name="RepairInvoicePDF"),
    url(r'^Repair/(?P<pk_No>\d+)/(?P<pk_RIR>\d+)/$',views.RepairItemRemove,name="RepairItemRemove"),
    url(r'^Repair/(?P<pk_No>\d+)/Delete/(?P<pk_Nod>\d+)/$',views.RepairDelete,name="Repairdelete"),

    url(r'^ChitBill/$',views.ChitBillOptions,name="ChitBillHome"),
    url(r'^ChitBill/New/$',views.ChitBillNew,name="ChitBillNew"),
    url(r'^ChitBill/Update/$',views.ChitBillUpdate,name="ChitBillUpdate"),
    url(r'^ChitBill/Update/(?P<pk_ChitBillID>\d+)/$',views.ChitBillUpdateid,name="ChitBillUpdateid"),
    url(r'^ChitBill/Update/(?P<pk_ChitBillID>\d+)/Close/$',views.ChitClose,name="ChitBillclose"),

    url(r'^BewareOfIncomeTaxOfficer/$',views.DangerAhead,name="Danger"),
]