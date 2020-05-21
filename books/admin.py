from django.contrib import admin

from .models import Ebook, Autor, Gendre, Publisher, Format, Banner, MainBanner, Cart, CartProduct, Order, OrderProduct

admin.site.register(Ebook)
admin.site.register(Autor)
admin.site.register(Gendre)
admin.site.register(Publisher)
admin.site.register(Format)
admin.site.register(Banner)
admin.site.register(MainBanner)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(OrderProduct)

def products(order):
    return [product for product in order.product.all()]

@admin.register((Order))
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','order_date',products,'total','payment_status']
    list_editable = ['payment_status']