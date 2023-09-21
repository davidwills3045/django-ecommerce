from django.shortcuts import render
from django.http import HttpResponse


def register_view(request):
    return render(request, "core/sign-up.html")
