from django.contrib import admin
from .models import Category,vendor,Product,Productimages,Cartorder,Cartorderitems,ProductReview,Wishlist,Address

class ProductimagesAdmin(admin.TabularInline):
    model = Productimages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductimagesAdmin]
    list_display = ["user","title","product_image","price","featured","product_status"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title","category_image"]

class VendorAdmin(admin.ModelAdmin):
    list_display = ["title","vendor_image"]

class CartorderAdmin(admin.ModelAdmin):
    list_display = ["user","price","paid_status","order_date","product_status"]

class CartorderitemsAdmin(admin.ModelAdmin):
    list_display = ["order","invoice_no","item","image","qty","price","total"]

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ["user","product","review","rating"]

class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user","product","date"]

class AddressAdmin(admin.ModelAdmin):
    list_display = ["user","address","status"]

admin.site.register(Category,CategoryAdmin)
admin.site.register(vendor,VendorAdmin)
admin.site.register(Product,ProductAdmin)
# admin.site.register(Productimages,ProductimagesAdmin)
admin.site.register(Cartorder,CartorderAdmin)
admin.site.register(Cartorderitems,CartorderitemsAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist,WishlistAdmin)
admin.site.register(Address,AddressAdmin)