from django.shortcuts import render
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from django.contrib.auth.models import User
from django.contrib import messages
from chatapp.models import Message
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from cryptography.fernet import Fernet

#used for security purposes(encryption and decryption)
key = Fernet.generate_key()
fernet = Fernet(key)

UserModel = get_user_model()
from .tokens import account_activation_token


# Create your views here.
def loginUser(request):
    
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request,user)
            return redirect("/")
            # A backend authenticated the credentials
        else:
            return render(request,'login.html')
            # No backend authenticated the credentials
    return render(request,'login.html')

def logoutuser(request):
    logout(request)
    return redirect('/accounts/login')

def signupuser(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        email=request.POST.get("email")
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already in use')
            return render(request,'signup.html')
        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already in use')
            return render(request,'signup.html')
        elif username=="":
            messages.warning(request, 'Invalid Username')
            return render(request,'signup.html')
        elif password=="":
            messages.warning(request, 'Invalid Password')
            return render(request,'signup.html')
        else:
            try:
                validate_email(email)
            except ValidationError as e:
               messages.warning(request, 'Invalid email address')
               return render(request,'signup.html')
            else:
                user = User.objects.create_user(username=username,password=password,email=email)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, 'Please confirm your email address to complete the registration')
                return redirect('/accounts/login')
    return render(request,'signup.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')
        return redirect('/accounts/login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('/accounts/login')


def forgotpassword(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        if User.objects.filter(username=username).exists()==False:
            messages.error(request,"Username doesn't exist")
            return redirect('/accounts/login')

        user=User.objects.get(username=username)
        if (user.is_active)==False:
            messages.error(request,"The username is not active")
            return redirect('/accounts/login')
        email=User.objects.get(username=username).email

        current_site = get_current_site(request)
        mail_subject = 'Reset your Password.'
        message = render_to_string('password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        })
        to_email = email
        email = EmailMessage(
        mail_subject, message, to=[to_email]
        )
        email.send()
        messages.success(request, 'Please check your registered email address to reset your password')
        return redirect('/accounts/login')
    
    return render(request, 'forgotpassword.html')

def passwordresetvalidation(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.save()
        return render(request, 'passwordreset.html', {'uid': fernet.encrypt((str(uid)).encode())})
    else:
        messages.error(request, 'password reset link is invalid!')
        return redirect('/accounts/login')

def passwordreset(request):
    if request.method =='POST':
        uid = str(request.POST.get("uid"))
        uid = uid[2:len(uid)-1]
        uid = bytes(uid, 'utf-8')
        uid = int(fernet.decrypt(uid).decode())
        new_password=request.POST.get("new_password")
        user=User.objects.get(pk=uid)
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Password changed successfully! Now you can login to your account')
        return redirect('/accounts/login')

    return redirect('/accounts/login')
