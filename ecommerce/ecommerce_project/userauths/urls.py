from django.urls import path
from .import views

urlpatterns = [
    path('sign-up/',views.register_view,name='sign-up'),
    path('sign-in/',views.login_view,name='sign-in'),
]