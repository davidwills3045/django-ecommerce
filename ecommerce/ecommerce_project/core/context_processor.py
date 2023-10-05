from .models import Category,Vendor,Product,Productimages,Cartorder,Cartorderitems,ProductReview,Wishlist,Address
from django.shortcuts import get_object_or_404

def default(request):
    categories = Category.objects.all()
    address = get_object_or_404(Address, user = request.user)
    return{
        "categories":categories,
        "address":address,
    }