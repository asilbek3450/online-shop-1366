from django.contrib import admin
from .models import Product, ProductCategory, ProductImage, UserModel, Comment, Wishlist, Cart, Order, OrderItem
# Register your models here.

admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(ProductImage)
admin.site.register(UserModel)
admin.site.register(Comment)
admin.site.register(Wishlist)
admin.site.register(Cart)
admin.site.register(Order)
