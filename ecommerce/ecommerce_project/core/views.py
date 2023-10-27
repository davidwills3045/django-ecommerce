from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import Category,Vendor,Product,Productimages,Cartorder,Cartorderitems,ProductReview,Wishlist,Address,Tags
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from django.db.models import Avg
from .forms import ProductReviewForm
from django.template.loader import render_to_string 


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

    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False

    p_image = product.p_image.all()

    context = {
        "make_review":make_review,
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

def search_view(request):
    query = request.GET.get("q")

    products = Product.objects.filter(title__icontains=query, description__icontains=query).order_by("-date")

    context = {
        "products":products,
        "query":query,
    }

    template = loader.get_template("search.html")
    return HttpResponse(template.render(context,request))

def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0 :
        products = products.filter(category__id__in=categories).distinct() #field look up
 
    if len(vendors) > 0 :
        products = products.filter(vendor__vid__in=vendors).distinct()

    data = render_to_string("async/product-list.html",{"products":products})
    return JsonResponse({"data": data})