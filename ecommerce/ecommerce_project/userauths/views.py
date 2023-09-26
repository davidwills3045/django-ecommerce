from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings
from .models import User

# User = settings.AUTH_USER_MODEL


def register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your account was successfuly created")
            new_user = authenticate(username=form.cleaned_data['email'],password= form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("index") 
    else:
        form = UserRegisterForm()

    context = {
        'form':form
    }
    return render(request, "userauths/sign-up.html",context)


def login_view(request):
    # print(request)

    if request.user.is_authenticated:
        messages.success(request, "Hey you are already logged in.")
        return redirect("index")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request,email=email,password=password)
            # request.session["user"] = user

            if user is not None:
                login(request,user)
                messages.success(request, "You are logged in.")
                # print(request.user.is_authenticated)
                return render(request,"index.html")
            else:
                messages.warning(request, "User Does Not Exist, Create an account.")
        except:
            messages.warning(request,f"User with {email} does not exist")

    return render(request,"userauths/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("sign-in")