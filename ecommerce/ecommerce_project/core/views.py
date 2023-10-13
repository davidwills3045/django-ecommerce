from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import Category,Vendor,Product,Productimages,Cartorder,Cartorderitems,ProductReview,Wishlist,Address,Tags
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from django.db.models import Avg
from .forms import ProductReviewForm


def index(request):
    # products = Product.objects.all()
    products = Product.objects.filter(product_status="published",featured=True)
    context = {
        "products":products
    }
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context,request))

def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    context = {
        "products":products
    }
    template = loader.get_template("product-filter.html")
    return HttpResponse(template.render(context,request))

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories":categories
    }
    template = loader.get_template("category-list.html")
    return HttpResponse(template.render(context,request))

def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published", category=category)

    context = {
        "category":category,
        "products":products,
    }

    template = loader.get_template("product-category-list.html")
    return HttpResponse(template.render(context,request))

def vendor_list_view(request):
    vendor = Vendor.objects.all()

    context = {
        "vendor":vendor,
    }

    template = loader.get_template("vendors-list.html")
    return HttpResponse(template.render(context,request))

def vendor_details_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status="published")
    context = {
        "vendor":vendor,
        "products":products,
    }

    template = loader.get_template("vendor-details-2.html")
    return HttpResponse(template.render(context,request))

def product_detail_view(request,pid):
    product = Product.objects.get(pid=pid)
    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    # Getting the reviews related to a product
    review = ProductReview.objects.filter(product=product)

    # Getting average review
    average_rating =  ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))


    # product review form
    review_form = ProductReviewForm()

    p_image = product.p_image.all()

    context = {
        "products":product,
        "p_image":p_image,
        "pro":products,
        "reviews":review,
        "average_rating":average_rating,
        "review_form":review_form,
    }
    template = loader.get_template("product-detail.html")
    return HttpResponse(template.render(context,request))

def tag_list(request, tag_slug=None):
    products= Product.objects.filter(product_status="published",).order_by("-id")

    tag= None
    if tag_slug:
        tag= get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {
        "products":products,
        "tag":tag,
    }
    template = loader.get_template("tag.html")
    return HttpResponse(template.render(context,request))

def  ajax_add_review(request,pid):
    product = Product.objects.get(pk=pid)
    user = request.user

    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating'],
    )

    context= {
        "user":user.username,
        "review":request.POST['review'] ,
        "rating":request.POST['rating'] ,
    }

    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
        {
        'bool':True,
        'context':context,
        'avg_reviews':average_reviews
        }
    )
