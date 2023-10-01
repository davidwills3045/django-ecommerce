from .models import Category,Vendor,Product,Productimages,Cartorder,Cartorderitems,ProductReview,Wishlist,Address

def default(request):
    categories = Category.objects.all()
    return{
        "categories":categories,
    }