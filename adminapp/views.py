from django.shortcuts import render,redirect
from fmiapp.models import Enquiry,logininfo,FarmerInfo,MerchantInfo
from . models import Booking,News
import datetime
# Create your views here.
def adminhome(request):
    try:
        if request.session['userid']:
         ns=News.objects.all()
         return render(request,'adminhome.html',{'ns':ns})
    except:
        return render(request,'login.html')

def enquiries(request):
    try:
        if request.session['userid']:
            enq = Enquiry.objects.all()
            return render(request,'enquiries.html',{'enq':enq})
    except:
        return render(request,'login.html')
def booking(request):
    try:
        if request.session['userid']:
         fi=FarmerInfo.objects.all()
         return render(request,'booking.html',{'fi':fi})
    except:
        return render(request,'login.html')


def purchase(request):
    try:
        if request.session['userid']:
          bk=Booking.objects.all()
          return render(request,'purchase.html',{'bk':bk})
    except:
        return render(request,'login.html')


def changepassword(request):
    try:
        if request.session['userid']:
         return render(request, 'changepassword.html')
    except:
        return render(request, 'login.html')


def logout(request):
        request.session['userid']=None
        return render(request,'login.html')


def Book(request,ano):
    fi=FarmerInfo.objects.get(aadharno=ano)
    return render(request,'Book.html',{'fi':fi})

def pbook(request):
    name=request.POST['name']
    address=request.POST['address']
    contactno=request.POST['contactno']
    aadharno=request.POST['aadharno']
    noofpacket=int(request.POST['noofpacket'])
    duration=int(request.POST['duration'])
    rate=int(request.POST['rate'])
    advance=int(request.POST['advance'])
    totalamt=noofpacket*duration*rate
    restamt=totalamt-advance
    bookingdate=datetime.datetime.today()
    b=Booking(name=name,address=address,contactno=contactno,aadharno=aadharno,noofpacket=noofpacket,duration=duration,rate=rate,advance=advance,totalamt=totalamt,restamt=restamt,bookingdate=bookingdate)
    b.save()
    msg='Booking is done'
    return redirect('adminapp:booking')
def viewbook(request,ano):
    res=Booking.objects.get(aadharno=ano)
    return render(request,'viewbook.html',{'res':res})
def deleteenq(request,id):
    e=Enquiry.objects.get(id=id)
    e.delete()
    return redirect('adminapp:enquiries')
def addnews (request):
    newstext=request.POST['newstext']
    newsdate=datetime.datetime.today()
    ns=News(newstext=newstext,newsdate=newsdate)
    ns.save()
    return redirect('adminapp:adminhome')
def deletenews(request,id):
    ns=News.objects.get(id=id)
    ns.delete()
    return redirect('adminapp:adminhome')
def changepwd(request):
    oldpassword=request.POST['oldpassword']
    newpassword=request.POST['newpassword']
    confirmpassword=request.POST['confirmpassword']
    msg='Message='
    if newpassword!=confirmpassword:
        msg=msg+'newpassword is not matched confirm password'
        return render(request,'changepassword.html',{'msg':msg})
    userid=request.session['userid']
    try:
        obj=logininfo.objects.get(userid=userid,password=oldpassword)
        logininfo.objects.filter(userid=userid).update(password=newpassword)
        return redirect('adminapp:logout')
    except:
        msg=msg+'oldpassword is not matched'
    return render(request,' changepassword.html',{'msg':msg})

def pay(request,ano):
    obj=Booking.objects.get(aadharno=ano)
    return render(request,'pay.html',{'obj':obj})
def paid(request):
    aadharno=request.POST['aadharno']
    restamt=int(request.POST['restamt'])
    payamt=int(request.POST['payamt'])
    restamt=restamt-payamt
    Booking.objects.filter(aadharno=aadharno).update(restamt=restamt)
    return redirect('adminapp:purchase')

