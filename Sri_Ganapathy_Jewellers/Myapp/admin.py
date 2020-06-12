from django.contrib import admin
from Myapp import models
# Register your models here.

admin.site.register(models.ShopCustomers)
admin.site.register(models.ShopHandlersSignUp)
admin.site.register(models.Stock)
admin.site.register(models.MaterialPricing)
admin.site.register(models.ChitBill)
admin.site.register(models.BillingItems)
admin.site.register(models.BillingPayment)
admin.site.register(models.StockAdd)
admin.site.register(models.StockPaid)
admin.site.register(models.PointTable)
admin.site.register(models.Repair)
admin.site.register(models.ChitBillUpdate)
admin.site.register(models.BalanceCheck_ToBePaid)
admin.site.register(models.Oldjewel)