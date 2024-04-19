from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect("movieapp:home")
    else:
        if request.method == "POST":
            form = RegistrationForm(request.POST or None)
            if form.is_valid():
                user=form.save()

                #get raw password:
                raw_password = form.cleaned_data.get('password1')

                #authenticate user:
                user= authenticate(username=user.username, password= raw_password)

                #login the user
                login(request,user)
                return redirect("movieapp:home")
        else:
            form = RegistrationForm()
        return render(request, "register.html", {"form":form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("movieapp:home")
    else:
        if request.method=="POST":
            username = request.POST['username']
            password = request.POST['password']

            #check the credentials
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect("movieapp:home")
                else:
                    return render(request,"login.html", {"error":"Your account has been disabled"})
            else:
                return render(request, "login.html", {"error":"Invalid Username or Password. Try again."})
        return render(request, 'login.html')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("movieapp:home")
    else:
        return redirect("credentials:login")


def my_view(request):
    username = None
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        if request.method == "POST":
            form = ProfileForm(request.POST or None, instance=user)
            if form.is_valid():
                data = form.save(commit=False)
                data.save()
                return redirect("movieapp:home")
        else:
            form = ProfileForm(instance = user)
        return render(request, "profile.html", {"form": form})
    else:
        return redirect("credentials:login")

