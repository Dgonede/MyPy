import textwrap
from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest

from .models import Category,Product,Order, OrderProduct


class ShortDescriptionMixin:
    @classmethod
    def short_descriptions(cls, obj:Category)-> str:
        return textwrap.shorten(obj.description, width=40)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, ShortDescriptionMixin):
    list_display = "pk", "name", "short_descriptions"
    list_display_links = "pk", "name",
    

class OrderTabularInline(admin.TabularInline):
    model = Product.orders.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ShortDescriptionMixin):
    inlines =[
        OrderTabularInline,
    ]
    list_display = "pk", "title", "price", "category", "short_descriptions", "available"
    list_display_links = "pk", "title",
    @admin.display(
        boolean=True,
    )
    def available(self, obj: Product)-> bool:
        return not obj.archived

class ProductTabularInline(admin.TabularInline):
    model = Order.products.through

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("order_products")
    inlines=[
        ProductTabularInline,
    ]
    list_display = "pk", "adress", "comment"
    list_display_links = "pk", "adress", "comment", 

  
@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "order", 
        "product", 
        "quantity", 
        "price",
        "total_price"
    )
    list_display_links = "pk",

