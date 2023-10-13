from django.urls import path
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

]