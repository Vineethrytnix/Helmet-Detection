from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth import authenticate
from django.contrib import messages
from main import process_video 
import os
# Create your views here.
#Hii

def index(request):
    
    return render(request, "index.html")
# def index(request):
    
#     return render(request, "index.html")


def log(request):
    if request.POST:
        email = request.POST["email"]
        passw = request.POST["password"]
        user = authenticate(username=email, password=passw)

        if user is not None:
            if user.userType == "Admin":
                messages.info(request, "Login Success")
                return redirect("/admin_home")
            elif user.userType == "User":
                id = user.id
                email = user.username
                request.session["uid"] = id
                request.session["email"] = email
                messages.info(request, "Login Success")
                return redirect("/user_home")
            else:
                messages.info(request, "type Not Defined")

        else:
            messages.error(request, "Invalid Username/Password")

    return render(request, "signin.html")


def reg(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        password = request.POST.get("password")

        if Login.objects.filter(username=email).exists():
            messages.error(request, "User already exists")
        else:
            new_user = Login.objects.create_user(
                username=email,
                password=password,
                email=email,
                first_name=name,
                userType="User",
                viewPass=password,
            )
            user_info = Userreg.objects.create(
                name=name,
                email=email,
                phone=phone,
                address=address,
                loginid=new_user,
            )
            user_info.save()

            messages.success(request, "Registration successful. You can now log in.")
            return redirect("/login")

    return render(request, "signup.html")




def user_index(request):
    uid=request.session['uid']
    user_id=Userreg.objects.get(loginid=uid)
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        video_path = os.path.join(r'D:\VINEETH\PYTHON PROJECTS\PROJECT_2024\CMS\Helmet_Detection\Helmet_detection\images', file.name)  # Adjust the path as necessary

        with open(video_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        process_video(video_path, user_id)

    return render(request, 'User/index.html',{"user_id": user_id})

def view_date(request):
    uid=request.session['uid']
    user_id=Userreg.objects.get(loginid__id=uid)
    print("Userid: ",user_id)
    view=Helmet.objects.filter(uid=user_id)
    print("view:",view)
    return render(request, 'User/view_data.html',{"view":view})


def udp(request):
    av=Helmet.objects.all().delete()
    return HttpResponse("Hello")