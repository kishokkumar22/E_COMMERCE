from django.http import HttpResponse
from ecommerce.form import CustomUserCreationForm
from django.shortcuts import redirect, render
from .models import*
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request) :
    products = Product.objects.filter(trending=1)
    return render(request,"ecommerce/index.html",{'products':products}) 

def logout_page(request) :
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'You are now logged out')
    return redirect('/')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user =authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'You are now logged in')
                return redirect('/')
            else:
                messages.error(request,'Username or Password is incorrect')
                return redirect("login")
        return render(request, "ecommerce/login.html")



def register(request) :
    form = CustomUserCreationForm
    if request.method=='POST' :
        form =CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Created Successfully')
            return redirect('login')
    return render(request,"ecommerce/register.html",{'form' : form})

def collections(request) :
    catagory = Catagory.objects.filter(status=1)
    return render(request,"ecommerce/collections.html",{'catagory':catagory})

def collectionviews(request,name) :
   if( Catagory.objects.filter(name =name,status=1)) :
       products = Product.objects.filter(catagory__name = name)
       return render(request,"ecommerce/products/index.html",{'products':products,'catagory_name':name})
   
   else :
       messages.warning(request,"No such Catagory Found")
       return redirect('collections')

def product_details(request,cname,pname) :
   if( Catagory.objects.filter(name =cname,status=1)) :
       if(Product.objects.filter(name=pname,status=1)) :
           products = Product.objects.filter(name=pname,status=1).first()
           return render(request, "ecommerce/products/product_details.html",{"products":products})
       else :
            messages.warning(request,"No such Product Found")
            return redirect('collections')
                
   else :
       messages.warning(request,"No such Catagory Found")
       return redirect('collections')
 