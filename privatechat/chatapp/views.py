from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import logout,login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Message,Friend,Fileupload
from django.http import JsonResponse

# Create your views here.

def home(request):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    return render(request, 'home.html')

def room(request,friendusername):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    if request.user.username == friendusername:
        return redirect('/')
    return render(request, 'room.html',{'friend':friendusername})

def checkview(request):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    if request.method == 'POST':
        friendusername =request.POST.get("friendusername")
        if request.user.username==friendusername:
            return redirect('/')
        if User.objects.filter(username=friendusername).exists():
            return redirect('/room/'+friendusername)
        else:
            return redirect('/')
    
    return redirect('/')

def send(request):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    if request.method == 'POST':
        sender=request.POST.get("username")
        receiver=request.POST.get("friend")
        message=request.POST.get("message")
        message=message.strip()
        if (message == "") or (request.user.username != sender):
            return redirect('/room/'+receiver)
        if sender==receiver:
            return redirect('/')
        newmessage=Message(sender=sender,receiver=receiver,message=message)
        newmessage.save()

        return HttpResponse("message sent")

    return redirect('/')

def getmessages(request,friend):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    if User.objects.filter(username=friend).exists()==False:
        return redirect('/')
    if request.user.username==friend:
        return redirect('/')
    all_messages=Message.objects.all().filter(sender=request.user).filter(receiver=friend)|Message.objects.all().filter(sender=friend).filter(receiver=request.user)

    return JsonResponse({"messages":list(all_messages.values())})


def friends(request):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    if request.method=='POST':
        friend=request.POST.get('friendusername')
        nickname=request.POST.get('friendnickname')
        user=request.user.username
        if friend==user:
            return redirect('/friends')
        if friend=="" or nickname=="":
            return redirect('/friends')
        if Friend.objects.filter(friend=friend).filter(user=user).exists():
            return redirect('/friends')
        if User.objects.filter(username=friend).exists()==False:
            return redirect('/friends')
        new_friend=Friend.objects.create(user=user, nickname=nickname,friend=friend)
        new_friend.save()
    
    unsorted_friends=Friend.objects.all().filter(user=request.user.username)
    user_friends=sorted(list(unsorted_friends.values()),key=lambda k:k['nickname'].lower())
    return render(request,'friends.html',{"user_friends": user_friends})


def removefriend(request):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')
    
    if request.method =='POST':
        friend=request.POST.get('friendusername')
        user=request.user.username
        if Friend.objects.all().filter(friend=friend).filter(user=user).exists()==False:
            return redirect('/friends')

        remove_friend=Friend.objects.all().filter(friend=friend).filter(user=user)
        remove_friend[0].delete()
        return redirect('/friends')

    return redirect('/friends')


def uploadfiles(request, friend):
    if request.user.is_anonymous or request.user.is_active==False:
        return redirect('/accounts/login')

    if(request.method=='POST'):
        sender= request.user.username
        receiver=friend
        if ('file' in request.FILES)==False:
            return redirect('/room/'+friend)
        file=request.FILES.get('file')
        new_file=Fileupload(file=file)
        new_file.save()

        file_name=new_file.file.name
        #file_name=file_name[15:len(file_name):1]

        new_message=Message(sender=sender,receiver=receiver,message=new_file.file.url,file_status=True,file_name=file_name)
        new_message.save()


    
    return HttpResponse('File uploaded successfully!')
