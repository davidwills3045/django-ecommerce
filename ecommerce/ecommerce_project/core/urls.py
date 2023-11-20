from django.urls import path,include
from .import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),
    path('product/', views.product_list_view, name='product-list'),
    path('product/<pid>/', views.product_detail_view, name='product-detail'),

    # Category
    path('category/', views.category_list_view, name='category-list'),
    path('category/<cid>/', views.category_product_list_view, name='category-product-list'),

    # Vendor
    path('vendor/', views.vendor_list_view, name='vendor-list'),
    path('vendor/<vid>/', views.vendor_details_view, name='vendor-details'),

    # Tags
    path('products/tag/<tag_slug>/', views.tag_list, name='tags'),

    # Add Review
    path('ajax-add-review/<int:pid>', views.ajax_add_review, name='ajax-add-review'),

    #search
    path('search/', views.search_view, name='search'),

    # filter product 
    path('filter-product/', views.filter_product, name='filter-product'),

    # add to cart
    path('add-to-cart/', views.add_to_cart, name='add_to-cart'),

    # cart page url
    path('cart/', views.cart_view, name='cart_view'),

    # delete from cart
    path('delete-from-cart/', views.delete_item_form_cart, name='delete-from-cart'),

    # update from cart
    path('update-cart/', views.update_cart, name='update-cart'),

    # checkout
    path('checkout/', views.checkout_view, name='checkout'),

    path('paypal/', include('paypal.standard.ipn.urls')),

    # payment succesful
    path('payment-completed/', views.payment_completed_view, name='payment-completed'),

    # payment failed
    path('payment-failed/', views.payment_failed_view, name='payment-failed'),
]