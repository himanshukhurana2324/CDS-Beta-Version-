from django.contrib import messages
from django.shortcuts import render, redirect 
from user.models import signup
from django.contrib.auth.models import auth
# Create your views here.
def login(request):
    return render(request,"login.html")


def register(request):

    if request.method == "POST":
        username = request.POST.get("username")
        print(f"UserName : {username}")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        bloodGroup = request.POST.get("bloodGroup")
        email = request.POST.get("email")
        state = request.POST.get("state")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")

        if password == cpassword:
            if signup.objects.filter(email=email).exists():
                messages.info(request,'Email already exists')
                return redirect('login')
            else:
                user = signup(email=email, username=username, age=age, bloodGroup=bloodGroup, gender=gender, state=state)
                user.set_password(password)
                user.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('login')
        

def signedin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')
    