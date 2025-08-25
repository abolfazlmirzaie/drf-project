from django.contrib import admin
from . models import OrderItem, Order
# Register your models here.




class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline,
    ]


admin.site.register(Order, OrderAdmin)