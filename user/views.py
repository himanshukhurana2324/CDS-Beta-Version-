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

        user = signup(email=email, username=username, age=age, bloodGroup=bloodGroup, gender=gender, state=state)
        user.set_password(password)
        user.save()
        print('user created')
        return redirect('home/')
    