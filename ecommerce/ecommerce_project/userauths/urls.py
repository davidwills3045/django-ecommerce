from django.urls import path
from .import views

urlpatterns = [
    path('signup/',views.register_view,name='sign-up'),
    path('signin/',views.login_view,name='sign-in'),
]