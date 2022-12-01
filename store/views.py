from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
#pagination
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
#Models
from .forms import ReviewForm
#cart
from cart.views import _cart_id
from cart.models import CartItems
#store
from store.models import Product,ReviewRating, Author
#category
from category.models import Category
#Wishlist
from wishlist.models import WishlistItems
#authentication
from authentication.models import UserProfile
#orders
from orders.models import OrderProduct

# Create your views here.


def product(request, category_slug = None):
    categories = None
    products = None

    # total_data = Product.objects.count()
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:    
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    
    context = {
        'products' : paged_products,
        
        # 'total_data' : total_data,
    }
    return render(request, 'store/product.html', context)




def product_details(request, category_slug, product_slug):
    wishlist=None
    try:
        if category_slug != None:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=categories, is_available=True)
            
        else:    
            products = Product.objects.all().filter(is_available=True)
        
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        in_cart = CartItems.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        if request.user.is_authenticated:
            wishlist = WishlistItems.objects.filter(product=single_product, user=request.user)
            if UserProfile.objects.filter(user_id=request.user.id):
                userprofile = UserProfile.objects.get(user_id=request.user.id)
            else:
                userprofile = None
            
        
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context = {
        'single_product' : single_product,
        'products' : products,
        'in_cart' : in_cart,
        'wishlist' : wishlist,
        'userprofile' : userprofile,
        'orderproduct' : orderproduct,
        'reviews' : reviews,
        'categories':categories,
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




def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! You review has been updated.")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! You review has been submitted.")
                return redirect(url)



def author_details(request, author_slug):
    author = None
    products = None
    # total_data = Product.objects.count()
    if author_slug != None:
        print('555555555555555555555')
        author = get_object_or_404(Author, slug=author_slug)
        products = Product.objects.filter(author=author, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:    
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 4)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    
    context = {
        'products' : paged_products,
        # 'total_data' : total_data,
    }
    return render(request, 'store/product.html', context)
