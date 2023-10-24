from .models import Category,Vendor,Product,Productimages,Cartorder,Cartorderitems,ProductReview,Wishlist,Address
from django.shortcuts import get_object_or_404
from django.db.models import Count,Min,Max

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()

    min_max_price =Product.objects.aggregate(Min("price"), Max("price"))

    try:
        address = get_object_or_404(Address, user = request.user)
    except:
        address = None
    return{
        "vendors":vendors,
        "categories":categories,
        "address":address,
        "min_max_price":min_max_price
    }