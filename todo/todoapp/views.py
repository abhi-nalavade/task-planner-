from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from todoapp.form import RegisterForm
from django.contrib.auth.models import User
from todoapp.models import Task
import datetime
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
import random
from django.core.mail import send_mail



# Create your views here.

def checkEmail(request):
    print(request.POST)

    #otp generation
    otp=random.randrange(1000,9999) 
    print("otp generation:",otp) 
    v=verify.objects.create(gmail=request.POST['email'],otp=otp)
    v.save()

def dashboard(request):
    content={}
    
     #fetch data from form
    if request.method=="POST":
        name=request.POST['tname']
        det=request.POST['tdetails']
        c=request.POST['cat']
        s=request.POST['status']
        dt=request.POST['duedate']

        #validation
        u=User.objects.filter(id=request.user.id)# fetch auth_user object
        t=Task.objects.create(name=name,detail=det,cat=c,status=s,enddate=dt,created_on=datetime.datetime.now(),uid=u[0])
        t.save()
        return redirect('/dashboard')


        return HttpResponse("in post section")


    else:
        q1=Q(uid=request.user.id)
        q2=Q(is_deleted=False)
        t=Task.objects.filter(q1 & q2)
        # print(t)
        sendpendingemail(t)
        content['data']=t
        return render(request,'todoapp/dashboard.html',content)


def user_register(request):
    content={}
    if request.method=="POST":
        un=request.POST['uname']
        p=request.POST['upass']
        cp=request.POST['ucpass']
        #validation
        if un=='' or p=='' or cp=='':
            content['errmsg']="Field Cannot Empty"
        elif p!=cp:
            content['errmsg']="password doesnt match"
        elif len(p)<8:
            content['errmsg']="Password must be 8 charecter in length"
        else:
            
            try:
                u=User.objects.create(username=un,email=un)
                u.set_password(p)
                u.save()
                content['success']="user register successfully!"
            except Exception:
                content['errmsg']="User with same name Already Exist"
        return render(request,'accounts/register.html',content)
    else:
        
        return render(request,'accounts/register.html')


def user_login(request):
    content={}
    if request.method=="POST":
        un= request.POST['uname']
        p= request.POST['upass']
        u=authenticate(username=un,password=p)
        # print(u)
        if u is not  None:
            login(request,u)
            return redirect('/dashboard')
        else:
            content['errmsg']="invalid username  or password"
            return render(request,'accounts/login.html',content)
    else: 
        return render(request,'accounts/login.html')


def user_logout(request):
    logout(request) # distroy or delete all the data from session
    return redirect('/login')

def delete(request,rid):
    #print("ID",rid)
    t=Task.objects.filter(id=rid)
    t.update(is_deleted=True)
    return redirect('/dashboard')

def edit(request,rid):
    if request.method=="POST":
        uname=request.POST['tname']
        udet=request.POST['tdetails']
        uc=request.POST['cat']
        us=request.POST['status']
        udt=request.POST['duedate']
        t=Task.objects.filter(id=rid)
        t.update(name=uname,detail=udet,cat=uc,status=us,enddate=udt)

        return redirect('/dashboard')
    else:
        #print("ID",rid)
        t=Task.objects.filter(id=rid)
        content={}
        content['data']=t
        return render(request,'todoapp/edit.html',content)
    
def catfilter(request,cv):
    q1=Q(uid=request.user.id)
    q2=Q(is_deleted=False)
    q3=Q(cat=cv)

    t=Task.objects.filter(q1 & q2 & q3)
    content={}
    content['data']=t
    return render(request,'todoapp/dashboard.html',content)  

def statfilter(request,sv):
    q1=Q(uid=request.user.id)
    q2=Q(is_deleted=False)
    q3=Q(status=sv)

    t=Task.objects.filter(q1 & q2 & q3)
    content={}
    content['data']=t
    return render(request,'todoapp/dashboard.html',content)   

def datefilter(request):
    frm=request.GET['from']
    to=request.GET['to']
    # print(frm)
    # print(to)
    q1=Q(uid=request.user.id)
    q2=Q(is_deleted=False)
    q3=Q(enddate__gte=frm)
    q4=Q(enddate__lte=to)
    t=Task.objects.order_by('-enddate').filter(q3 & q4).filter(q1 & q2)
    content={}
    content['data']=t

    return render(request,'todoapp/dashboard.html',content)

def datefilter2(request,dv):
    if dv==0:
        p='enddate'
    else:
        p='-enddate'


    t=Task.objects.filter().order_by(p)
    content={}
    content['data']=t

    return render(request,'todoapp/dashboard.html',content)

def datesort(request,dv):
    q1=Q(uid=request.user.id)
    q2=Q(is_deleted=False)
    if dv=='0':
        col='-enddate'
    else:
        col='enddate'
    
    t=Task.objects.order_by(col).filter(q1 & q2)
    
    content={}
    content['data']=t

    
    return render(request,'todoapp/dashboard.html',content)

    
def sendpendingemail(t):
    print("In pending email")

    for x in t:
        if x.status==0:
            d=x.enddate.day
            # print(d)
            curdt=datetime.datetime.now().day
            
            diff=d-curdt
            # print(diff)
            if diff==1:
                rec=x.uid.email
                print(rec)
                subject="REMAINDER"
                msg=x.name+" Task is due for 1 day "
                sender='harshalbhole9@gmail.com'
                send_mail(
                subject,
                msg,
                sender,
                [rec],
                fail_silently=False
                )
