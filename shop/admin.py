from django.contrib import admin

# Register your models here.
from .models import Product, Contact, Orders, OrderUpdate, Comments

admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register((Product, Comments))