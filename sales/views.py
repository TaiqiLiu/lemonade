
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from .models import Record, Staff, Beverage, User

from functools import wraps
from django.utils import timezone


#Use this function on each page to check whether uesr is logged in, and jump if not logged in.
def check_login(f):
    @wraps(f)
    def inner(request,*arg,**kwargs):
        if request.session.get('is_login')=='1':
            return f(request,*arg,**kwargs)
        else:
            return redirect('/sales/login/')
    return inner

#index page, return username to index.html in this function
@check_login
def index(request):

    user_id1=request.session.get('user_id')
    userobj=User.objects.filter(id=user_id1)

    if userobj:
        return render(request,'sales/index.html',{"user":userobj[0]})
    else:
        return render(request,'sales/index.html',{'user','anonymous'})




#Receive and process forms.
#If the content of the form is incorrect, the reason for the error is returned.
#If the content of the form is correct, add the content to the database.
@check_login
def form(request):       
    error_msg = ""
    if request.method=="POST":
        boo=True
        getname = request.POST.get('name',"")
        getbeverage = request.POST.get('beverage',"")
        getquantity = request.POST.get('quantity', "")
        if Staff.objects.filter(name=getname).count() == 0:
            error_msg = "Name doesn't exist"
            boo = False
        if Beverage.objects.filter(Beverage_text=getbeverage).count() ==0:
            error_msg = "Beverage doesn't exist"
            boo = False
        if not(getquantity.isdigit()):
            error_msg = "Quantity is not correct"
            boo = False
        if (getname == "") | (getbeverage == "") | (getquantity == ""):
            error_msg = "Incomplete data input"
            boo = False
        if boo == True:           #When the content of the form meets the filter, add it to database
            newRecord = Record(name=getname,Beverage_text=getbeverage,pub_date=timezone.now(),quantity=getquantity)
            newRecord.save()
            return render(request,'sales/form.html',{"error_msg": "succeed!"})

    return render(request,'sales/form.html',{"error_msg": error_msg})

@check_login
def report(request):
    return render(request, 'sales/report.html')


#Receive the filtering conditions provided by report.html, 
#find qualified data from the database,
#store the qualified data in a string, 
# and return the string to the client.
@check_login
def showreport(request):
    name = request.POST.get("name")
    
    if Staff.objects.filter(name=name).count() == 0:
        return HttpResponse("This employee does not exist")
    if Record.objects.filter(name=name).count() == 0:
        return HttpResponse("No record for this employee")
    
    startdate = request.POST.get("startdate")
    enddate = request.POST.get("enddate")
    cart = Record.objects.filter(name=name)
    #开始时间判断cart
    #结束时间判断cart
    recordText = ''
    if len(cart) > 0:            
        q1=Staff.objects.get(name=name)
        rate = q1.commission/100              
        total = 0
        i = 0
        arr=['1234','/n','qwer','asdf']
        for current in cart:
            q2 = Beverage.objects.get(Beverage_text=current.Beverage_text)
            price = q2.price
            quantity = current.quantity
            recordText = recordText + current.pub_date.strftime('%m/%d/%Y %H:%M')
            recordText = recordText + '---------'
            recordText = recordText + current.Beverage_text
            recordText = recordText + '---------' 
            recordText = recordText + str("%.2f" %(price*quantity))
            total = total + price*quantity
            recordText = recordText + '---------'
            recordText = recordText + str("%.2f" %(price*rate*quantity))
            recordText = recordText + '---------'
            i = i + 1
        recordText = recordText + 'Commission = '+str("%.2f" %(rate*100))+'%---------'
        recordText = recordText + 'Total Price = ' + str("%.2f" %total)+'---------'
        recordText = recordText + 'Total Commission = ' + str("%.2f" %(total*rate))    
        return HttpResponse(recordText)
        #return render(request,'showreport.html',{"recordText": recordText})
    else:
        return HttpResponse("No Record")


#Receive and process data from the login interface
def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username,password=password)
        print(user)
        if user:
           
            request.session['is_login']='1'  # Other pages are used to determine whether logged in
            request.session['user_id']=user[0].id
            return redirect('/sales')

    return render(request,'sales/login.html')




