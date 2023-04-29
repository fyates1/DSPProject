from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout

def login_view(request):
    form = LoginForm(request.POST)
    message = None
    if request.method== 'POST':
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                nxt = request.GET.get("next", None)
                if nxt is not None:
                    return redirect(str(nxt))
                else:
                    return redirect('home')
            else:
                message = "Invalid Credentials"
        else:
            message = "Error In Form"
    return render(request, "login.html",{"form": form , "message":message})

def logout_user(request): 
    logout(request)
    return redirect('home')

def register_user(request):
    msg = None
    if request.method =="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = "User Created"
            return redirect("login_view")
        else:
            msg="Form is not valid"
    else:
        form = SignUpForm()
    return render(request,"register.html",{"form": form, "message":msg})
    
def home(request):
    return render(request,"home.html")

