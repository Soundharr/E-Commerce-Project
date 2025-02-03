from http.client import HTTPResponse
from django.shortcuts import redirect, render,  get_object_or_404
from shop.form import CustomUserForm


from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from . models import *

# Create your views here.

def home(request):
    return render(request,"shop/index.html")

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logged Out Successfully!")
    return redirect("/")
        

def login_page(request):
    if request.user.is_authenticated:  # Corrected the typo here
        return redirect("/")
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request, username=name, password=pwd)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('/login')
    return render(request, "shop/login.html")
    

def register(request):
    form = CustomUserForm()
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can log in now.")
            return redirect('/login')
        else:
            messages.error(request, "There were errors in your registration form.")
    return render(request, "shop/register.html", {'form': form})


def collections(request):
    catagory=Catagory.objects.filter(status=0)
    return render(request,"shop/collections.html",{"catagory":catagory})


"""def collectionsview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(Catagory__name=name)
        return render(request,"shop/products/index.html",{"products":products})
    else:
        messages.warning(request,"Not Found ")
        return redirect('collections')"""
        
def collectionsview(request, name):
    # Correct the filter to use lowercase 'catagory'
    if Catagory.objects.filter(name=name, status=0):
        products = Product.objects.filter(catagory__name=name)  # Use 'catagory' as the field name
        print(products,"collectionview")
        return render(request, "shop/products/index.html", {"products": products,"catagory_name":name})
        #return render(request, "shop/products/index.html", {"products": products})

    else:
        c=messages.warning(request, "Category Not Found")
        print(c,"helooooo")
        return redirect('collections')

"""from django.template import loader
def product_details(request, cname, pname):
    # Check if category exists and is active (status=0)
    category_exists = Catagory.objects.filter(name=cname, status=0).exists()

    if category_exists:
        # If category exists, filter products by name (case-insensitive) and active status
        products = Product.objects.filter(catagory__name=cname, name__iexact=pname, status=0)

        if products.exists():
            # If products exist, render the product details page
            print(list(products), "product_details")  # This will help in debugging
            return render(request, 'shop/products/porduct_details.html', {"products": products})
        else:
            # If no matching products found, show a warning message and redirect to collections
            messages.warning(request, "Product Not Found")
            return redirect('collections')
    else:
        # If category doesn't exist or is hidden, show a warning and redirect
        messages.warning(request, "Category Not Found")
        return redirect('collections')"""



def product_details(request, cname, pname):
    # Check if category exists
    category_exists = Catagory.objects.filter(name=cname, status=0).exists()
    if category_exists:
        # Check if product exists in the category
        products = Product.objects.filter(name__iexact=pname, status=0)
        if products.exists():
            print(list(products), "product_details")  # Evaluate the queryset
            return render(request, 'shop/products/product_details.html', {"products": products})
                                   #shop/products/porduct_details.html
        else:
            messages.warning(request, "Product Not Found")
            return redirect('collections')
    else:
        messages.warning(request, "Category Not Found")
        return redirect('collections')

