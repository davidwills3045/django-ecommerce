from .models import Category,Vendor,Product,Productimages,Cartorder,Cartorderitems,ProductReview,Wishlist,Address

def default(request):
    categories = Category.objects.all()
    # address = Address.objects.get(user=request.user)
    return{
        "categories":categories,
        # "address":address,
    }