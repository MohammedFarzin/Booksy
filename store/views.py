from django.shortcuts import render, get_object_or_404
from category.models import Category
from cart.models import CartItems
from cart.views import _cart_id
from store.models import Product
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.


def product(request, category_slug = None):
    categories = None
    products = None

    # total_data = Product.objects.count()
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:    
        products = Product.objects.all().filter(is_available=True).order_by('id')
    context = {
        'products' : products,
        # 'total_data' : total_data,
    }
    return render(request, 'store/product.html', context)




def product_details(request, category_slug, product_slug):
    try:
        if category_slug != None:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=categories, is_available=True)
            
        else:    
            products = Product.objects.all().filter(is_available=True)
        
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        in_cart = CartItems.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e

    context = {
        'single_product' : single_product,
        'products' : products,
        'in_cart' : in_cart,
    }
    return render(request, 'store/product_detail.html', context)



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
    context = {
        'products' : products,
    }
    return render(request, 'store/product.html', context)

