from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Category,Vendor,Product,Productimages,Cartorder,Cartorderitems,ProductReview,Wishlist,Address


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