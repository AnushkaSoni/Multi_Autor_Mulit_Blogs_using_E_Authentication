from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
import datetime
from django.urls import reverse
from random import randint
from django.core.mail import send_mail,EmailMessage
from django.conf import settings
import qrcode,pyzbar
from django.views.decorators.cache import cache_control

data = []
code_generated = 0

location = "D:/Major_Project/MultiBlogs/BlogSite/"

def index(request):
    return render(request, 'index.html', {'name': None})


def login(request):
    if request.method == 'POST':
        loginusername = request.POST.get('username')
        loginpassword = request.POST.get('password')
        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            user = User.objects.get(username=loginusername)
            user_email = user.email
            if 'LoginBtn1' in request.POST:
                otp = randint(100000, 999999)
                print(otp)
                subject = "Login with OTP"
                sender = settings.EMAIL_HOST_USER
                message = "Hi,"+ str(user.first_name)+", this is your OTP for logging into our system : " + str(otp) + ". Please login within 5 minutes."
                val = send_mail(subject, message, sender, [user_email])
                if val:
                    print('Email was sent successfully')
                    request.session['username']=loginusername
                    request.session['password']=loginpassword
                    request.session['otp']=otp
                    return redirect('../OTP')
                else:
                    print('Email was not sent successfully')
                    return redirect('../login')
            elif 'LoginBtn2' in request.POST:
                qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=5,border=5)
                qr.add_data(loginusername + ' ' + loginpassword)
                qr.make(fit=True)
                img = qr.make_image(fill_color='black', back_color='white')
                img.save(location+'qrcode_'+str(user.username) +'.png')
                print('QR Code generated!!')
                
                email_sender = settings.EMAIL_HOST_USER
                subject = "Login with QR"
                message = "Hi,"+ str(user.first_name)+", the QR for logging into our system is attached. Please login within 5 minutes."
                mail = EmailMessage(subject,message,email_sender,[user_email])
                mail.attach_file(location+'qrcode_'+str(loginusername)+'.png')
                val = mail.send()
                if val:
                    print('Email was sent successfully')
                    request.session['username']=loginusername
                    request.session['password']=loginpassword
                    return redirect('../QR')
                else:
                    print('Email was not sent successfully')
                    return redirect('../login')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('../login')
    else:
        return render(request,'login.html')

def OTPAuthentication(request):
    if request.method == 'POST' and (request.session['username'] and request.session['password'] and request.session['otp']):
        OTP2 = request.POST['OTP']
        username = request.session['username']
        password = request.session['password']
        otp = request.session['otp']
        if (str(otp) == str(OTP2)):
            user=auth.authenticate(request,username=username,password=password)
            auth.login(request,user)
            return redirect('../../')
        else:
                print('Wrong OTP mentioned!!!')
                return redirect('../login') 
    elif (request.method == 'GET' and (request.session['username'] and request.session['password'])):
        return render(request,'loginwithOTP.html')
    else:
        return redirect('../../')

def QRAuthentication(request):
    if request.method == 'POST' and (request.session['username'] and request.session['password']):
        #Take the session variable
        username = request.session['username']
        password = request.session['password']

        #Take the variables from QR Code reader template
        credentials = request.POST['b']
        temp = credentials.split(" ")
        username2 = temp[0]
        password2 = temp[1]
        if (str(username)== str(username2) and str(password) ==str(password2)):
            user=auth.authenticate(request,username=username,password=password)
            auth.login(request,user)
            return redirect('../../')
        else:
           print('Invalid credentials!!!')
        return redirect('../login')
    elif request.method == 'GET' and (request.session['username'] and request.session['password']):
        return render(request,'loginwithQR.html')
    else:
        return redirect('../../')

"""
            login(request,user)
            messages.success(request,"Login Successful!!")
            return redirect('main')
        else:
            messages.warning(request,"Invalid Credentials.")
            return redirect('login')
    return render(request, 'login.html')
"""

def signin(request):
    return render(request, 'sign.html')


def verify_code(request):
    if request.method=='POST':
        code_recieved = request.POST.get('code')
        if str(code_generated) == code_recieved:
            newuser = User.objects.create_user(data[3], data[2], data[4])
            newuser.first_name = data[0]
            newuser.last_name = data[1]
            newuser.save()
            messages.success(request,"Signed up successfully!!")
            return redirect('login')
    return redirect('login')


def sendcode(request):
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    user = request.POST.get('user')
    password = request.POST.get('password')
    global data
    data = [fname, lname, email, user, password]
    newuser = User.objects.create_user(data[3], data[2], data[4])
    newuser.first_name = data[0]
    newuser.last_name = data[1]
    newuser.save()
    messages.success(request,"Signed up successfully!!")
    return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    auth.logout(request)
    request.session.flush()
    messages.success(request,"Logout Successful!!")
    return redirect('main')

def change_user(request):
    return HttpResponse("Change username")


def change_pass(request):
    return HttpResponse("Change password")

def about(request):
    return render(request,'about.html')
