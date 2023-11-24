from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.template import loader
from .models import Category,Vendor,Product,Productimages,Cartorder,Cartorderitems,ProductReview,Wishlist,Address,Tags
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from django.db.models import Avg
from .forms import ProductReviewForm
from django.template.loader import render_to_string 
from django.contrib import messages

from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
import datetime

@login_required
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

def add_to_cart(request):
    cart_product = {}

    #getting the current product id
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }

    # checking of the cart data is available in the cart

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product

    return JsonResponse({
        "data":request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        })


def cart_view(request):
    cart_total_amount = 0
    if "cart_data_obj" in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "cart.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})  
    else:
        # return render(request, "cart.html",{'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})  
        messages.warning(request, "Your Cart is empty")
        return redirect("index")

def delete_item_form_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if "cart_data_obj" in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context,'totalcartitems': len(request.session['cart_data_obj'])})

def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if "cart_data_obj" in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("cart-list.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})
    return JsonResponse({"data":context,'totalcartitems': len(request.session['cart_data_obj'])})

@login_required
def checkout_view(request):

    cart_total_amount = 0
    total_amount = 0

    #checking if cart_data_obj session exists
    if "cart_data_obj" in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            total_amount += int(item['qty']) * float(item['price'])     

        # creating order object
        order = Cartorder.objects.create(
            user = request.user,
            price=total_amount
        )
        
        # getting total amount for the cart
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price']) 

            cart_order_products  = Cartorderitems.objects.create(
                order = order,
                invoice_no = "INVOICE_NO-"+ str(order.id),
                item = item['title'],
                image = item['image'],
                qty = item['qty'],
                price = item['price'],
                total = float(item['qty']) * float(item['price'])

            )
    

    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount':cart_total_amount,
        'item_name': 'Order-Item-No-'+ str(order.id),
        'invoice': 'INV_NO-'+ str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment-completed')),
        'cancel_url': 'http://{}{}'.format(host, reverse('payment-failed')),
    }

    # Form to render the paypal button
    paypal_payment_button = PayPalPaymentsForm(initial=paypal_dict)

    cart_total_amount = 0
    if "cart_data_obj" in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "checkout.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount, 'paypal_payment_button':paypal_payment_button})  

@login_required 
def payment_completed_view(request):
    issue_date = datetime.datetime.now()
    cart_total_amount = 0
    if "cart_data_obj" in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    # return render(request,'payment-completed.html')
    return render(request, "payment-completed.html",{"cart_data":request.session['cart_data_obj'],'totalcartitems': len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount,'issue_date':issue_date})  


@login_required
def payment_failed_view(request):
    return render(request,'payment-failed.html')


def account(request):
    template = loader.get_template("account.html")
    return HttpResponse(template.render())

def about(request):
    template = loader.get_template("about.html")
    return HttpResponse(template.render())

def contact(request):
    template = loader.get_template("contact.html")
    return HttpResponse(template.render())