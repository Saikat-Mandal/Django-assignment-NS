from django.shortcuts import render

# Create your views here.
from django.shortcuts import render , redirect
from .models import *
from django.http import HttpResponse
from django.core.paginator import Paginator
from decimal import Decimal , InvalidOperation
# from django.contrib.auth.models import User
from django.contrib.auth import  logout
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse, get_object_or_404


from .models import User, Product, Recommendation


# get all products 

def get_all_products(request):

    if request.method == 'POST':
        shape = request.POST.get('shape')
        size = request.POST.get('size')
        location = request.POST.get('location')
        price_str = request.POST.get('price')
        price = Decimal(price_str)
        product = Product.objects.create( shape=shape, size=size, location=location, price=price)
        product.save()
        return redirect('/dashboard')

    product_list = Product.objects.order_by('id')  
    paginator = Paginator(product_list, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if 'user_id' not in request.session:
        return redirect('/')
    user_id = request.session.get('user_id')
    return render(request, 'dashboard.html', {'page_obj': page_obj , 'user_id' : user_id})

@csrf_exempt
def product_viewed(request, product_id):
        user_id = request.session.get('user_id')
        if not user_id or not product_id:
            return HttpResponse("Invalid user ID or product ID.", status=400)

        user = get_object_or_404(User, pk=user_id)
        product = get_object_or_404(Product, pk=product_id)

        similar_products = Product.objects.filter(shape=product.shape)[:5]

        for similar_product in similar_products:

            existing_recommendation = Recommendation.objects.filter(user=user, product=similar_product).exists()
            if not existing_recommendation:
                recommendation = Recommendation(user=user, product=similar_product)
                recommendation.save()


        product = Product.objects.get(id=product_id)
        return render(request, 'product.html' , {'product' : product} )


    
# get product by id 
def get_product_by_id(request , id):
    queryset = Product.objects.get(id)
    return render(request , '' , {'products' : queryset})

# delete a product by id 
def delete_by_id(request , id):
    Product.objects.get(id=id).delete()
    return redirect('/dashboard')

# update a product by id 
def update_by_id(request , id):
    product = Product.objects.get(id=id)

    if request.method == 'POST':
        shape = request.POST.get('shape')
        size = request.POST.get('size')
        location = request.POST.get('location')
        price_str = request.POST.get('price')

        # Convert price string to Decimal if provided and valid
        if price_str:
            try:
                price = Decimal(price_str)
            except InvalidOperation:
                # Handle the case where the price string is invalid
                # For example, notify the user or set a default price
                price = Decimal(0)
        else:
            # Handle the case where no price is provided
            # For example, set a default price
            price = Decimal(0)

        # Update the product object with new values
        product.shape = shape
        product.size = size
        product.location = location
        product.price = price
        product.save()

        return redirect('/dashboard')
    
    return render(request, 'update.html' , {'product' : product})

# users 
def get_all_users(request):
    queryset = User.objects.all()
    return render(request , 'users.html' , {'user' : queryset})

# recommendation 
def recommendation_page(request,user_id):
    recommendations = Recommendation.objects.filter(user_id=user_id)
    return render(request, 'recommendation.html', {'recommendations': recommendations})


# login
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is not None and user.password == password:
            user = User.objects.get(username=username)
          
            request.session['user_id'] = user.id # Example of storing user ID in session
            return redirect('/dashboard')
        else:
            return redirect('/')

    return render(request, 'login.html')

# register
def register_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        age_str = request.POST.get('age')
        address = request.POST.get('address')
        name= request.POST.get('name')
        age = Decimal(age_str)
        if User.objects.filter(username=username):
            return redirect('/')

        user = User.objects.create(name = name, username = username , password = password ,age =age , address = address )
        user.save()

        return redirect('/')

    return render(request , 'register.html')


def logout_page(request):
    logout(request)
    return redirect('/')
