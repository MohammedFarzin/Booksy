from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required

# authentication
from authentication.models import Account
# category
from category.models import Category
# Store
from store.models import Product, Variation, Author, ReviewRating
# Order
from orders.models import Order, OrderProduct, Coupon
# Forms
from .forms import ProductForm, VariationForm, AuthorForm

# Create your views here.

# ADMIN DASHBOARD
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def adminpanel(request):
    if request.user.is_superadmin:

        user_count = Account.object.filter(is_superadmin=False).count()
        category_count = Category.objects.filter().count()
        product_count = Product.objects.filter().count()
        variation_count = Variation.objects.filter().count()
        order_count = OrderProduct.objects.filter(ordered=True).count()
        admin_order_count = Order.objects.filter(user__is_superadmin=True).count()

        context = {
            'user_count': user_count,
            'category_count': category_count,
            'product_count': product_count,
            'variation_count': variation_count,
            'order_count': order_count,
            'admin_order_count': admin_order_count,

        }

        return render(request, 'admin_panel/adminpanel.html', context)
    else:
        return redirect('home')

# ADMIN USER MANAGEMENT

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def user_management(request):
    if 'key' in request.GET:
        key = request.GET['key']
        print(key)
        users = Account.object.order_by('-id').filter(Q(first_name__icontains=key) | Q(email__icontains=key))
        print('if function')
    else:
        users = Account.object.filter(is_superadmin=False).order_by('id')
        print(users)

    paginator = Paginator(users, 4)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)

    context = {
        'users': paged_users,
    }
    return render(request, 'admin_panel/user_management.html', context)


@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def user_ban(request, user_id):
    user = Account.object.get(id=user_id)
    user.is_active = False
    user.save()
    return redirect('user_management')



@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def user_unban(request, user_id):
    user = Account.object.get(id=user_id)
    user.is_active = True
    user.save()
    return redirect('user_management')


# ADMIN CATEGORY MANAGEMENT
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def category_management(request):
    if request.method == 'POST':
        key = request.POST['keyword']
        categories = Category.objects.filter(Q(category_name__startswith=key) | Q(slug__startswith=key)).order_by('id')
    else:
        categories = Category.objects.all().order_by('id')

    paginator = Paginator(categories, 4)
    page = request.GET.get('page')
    paged_categories = paginator.get_page(page)

    context = {
        'categories': paged_categories
    }
    return render(request, 'admin_panel/category_management.html', context)



@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def add_category(request):
    if request.method == 'POST':
        try:
            category_name = request.POST['category_name']
            category_slug = request.POST['category_slug']
            category_description = request.POST['category_description']

            categories = Category(
                category_name=category_name,
                slug=category_slug,
                description=category_description
            )

            categories.save()
            return redirect('category_management')
        except Exception as e:
            raise e

    return render(request, 'admin_panel/add_category.html')



@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def update_category(request, category_id):
    try:
        categories = Category.objects.get(id=category_id)

        if request.method == 'POST':
            category_name = request.POST['category_name']
            category_slug = request.POST['category_slug']
            category_description = request.POST['category_description']

            categories.category_name = category_name
            categories.slug = category_slug
            categories.description = category_description

            categories.save()
            return redirect('category_management')

        context = {
            'category': categories,
        }
    except Exception as e:
        raise e

    return render(request, 'admin_panel/update_category.html', context)




@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def delete_category(request, category_id):
    categories = Category.objects.get(id=category_id)
    categories.delete()

    return redirect('category_management')


# ADMIN PRODUCT MANAGEMENT

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def product_management(request):
    if request.method == 'POST':
        key = request.POST['key']
        products = Product.objects.filter(Q(product_name__startswith=key) | Q(
            slug__startswith=key) | Q(category__category_name__startswith=key)).order_by('id')
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)

    context = {
        'products': paged_product,
    }
    return render(request, 'admin_panel/product_management.html', context)


@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        try:
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()

                return redirect('product_management')

        except Exception as e:
            raise e

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'admin_panel/edit_product.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_management')
    else:
        form = ProductForm()
        context = {
            'form': form
        }
        return render(request, 'admin_panel/add_product.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('product_management')
# ADMIN ORDER MANAGEMENT

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def order_management(request):
    if request.method == 'POST':
        key = request.POST['key']
        orders = Order.objects.filter(Q(is_ordered=True), Q(order_number__contains=key) | Q(user__email__contains=key) | Q(first_name__icontains=key)).order_by('id')
    else:
        orders = Order.objects.filter(is_ordered=True).order_by('id')

    paginator = Paginator(orders, 4)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)

    context = {
        'orders': paged_orders
    }
    return render(request, 'admin_panel/order_management.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def manager_cancel_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Cancelled'
    order.save()

    return redirect('order_management')

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def accept_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Shipped'
    order.save()

    return redirect('order_management')

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def complete_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Delivered'
    order.save()

    return redirect('order_management')

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def cancel_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    order.status = 'Cancelled'
    order.save()

    return redirect('admin_orders')


# ADMIN VARIATION MANAGEMENT
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def variation_management(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        variations = Variation.objects.filter(Q(product__product_name__icontains=keyword) | Q(variation_category__icontains=keyword) | Q(variation_values__icontains=keyword)).order_by('id')

    else:
        variations = Variation.objects.all().order_by('id')

    paginator = Paginator(variations, 4)
    page = request.GET.get('page')
    paged_variations = paginator.get_page(page)

    context = {
        'variations': paged_variations
    }
    return render(request, 'admin_panel/variation_management.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def add_variation(request):

    if request.method == 'POST':
        form = VariationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('variation_management')

    else:
        form = VariationForm()

    context = {
        'form': form
    }
    return render(request, 'admin_panel/add_variation.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def update_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)

    if request.method == 'POST':
        form = VariationForm(request.POST, instance=variation)
        if form.is_valid():
            form.save()
            return redirect('variation_management')

    else:
        form = VariationForm(instance=variation)

    context = {
        'variation': variation,
        'form': form
    }
    return render(request, 'admin_panel/update_variation.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def delete_variation(request, variation_id):
    variation = Variation.objects.get(id=variation_id)
    variation.delete()
    return redirect('variation_management')


# ADMIN AUTHOR MANGEMENT
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def author_management(request):
    if request.method == 'POST':
        keyword = request.POST['keyword']
        authors = Author.objects.filter(name__icontains=keyword).order_by('id')

    else:
        authors = Author.objects.all().order_by('id')

    paginator = Paginator(authors, 4)
    page = request.GET.get('page')
    paged_authors = paginator.get_page(page)

    context = {
        'authors': paged_authors
    }
    return render(request, 'admin_panel/author_management.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_management')
    else:
        form = AuthorForm()

    context = {
        'form': form
    }
    return render(request, 'admin_panel/add_author.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def update_author(request, author_id):
    author = Author.objects.get(id=author_id)

    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_management')

    else:
        form = AuthorForm(instance=author)

    context = {
        'author': author,
        'form': form
    }
    return render(request, 'admin_panel/update_author.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def delete_author(request, author_id):
    author = Author.objects.get(id=author_id)
    author.delete()
    return redirect('author_management')

# ADMIN ORDERS

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def admin_order(request):
    current_user = request.user
    try:

        if request.method == 'POST':
            keyword = request.POST['keyword']
            orders = Order.objects.filter(Q(user=current_user), Q(is_ordered=True), Q(order_number__contains=keyword) | Q(user__email__icontains=keyword) | Q(first_name__startswith=keyword) | Q(last_name__startswith=keyword) | Q(phone__startswith=keyword)).order_by('-created_at')

        else:
            orders = Order.objects.filter(
                user=current_user, is_ordered=True).order_by('-created_at')
    except Exception as e:
        raise e
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)
    context = {
        'orders': paged_orders,
    }
    return render(request, 'admin_panel/admin_order.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def admin_change_password(request):
    if request.method == 'POST':
        current_user = request.user
        current_password = request.POST['current_password']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if check_password(current_password, current_user.password):
                if check_password(password, current_user.password):
                    messages.warning(
                        request, 'Current password and new password is same')
                else:
                    hashed_password = make_password(password)
                    current_user.password = hashed_password
                    current_user.save()
                    messages.success(request, 'Password changed successfully')
            else:
                messages.error(request, 'Wrong password')
        else:
            messages.error(request, 'Passwords does not match')
    return render(request, 'admin_panel/admin_change_password.html')


# ADMIN REVIEW MANAGEMENT

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def review_management(request):
    if request.method == 'POST':
        key = request.POST['key']
        reviews = ReviewRating.objects.filter(Q(product__product_name__icontains=key), Q(status=True)).order_by('id')
    else:
        reviews = ReviewRating.objects.all()

    paginator = Paginator(reviews, 4)
    page = request.GET.get('page')
    paged_reviews = paginator.get_page(page)

    
    context = {
        'reviews': paged_reviews
    }
    return render(request, 'admin_panel/review_management.html', context)

@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def review_block(request, review_id):
  print("hai")
  review = ReviewRating.objects.get(id=review_id)
  review.status = False
  review.save()
  return redirect('review_management')


@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def review_unblock(request, review_id):
  review = ReviewRating.objects.get(id=review_id)
  review.status= True
  review.save()
  return redirect('review_management')



#COUPON MANAGEMENT
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def coupon_management(request):
    if request.method == 'POST':
        key = request.POST['key']
        coupon = Coupon.objects.filter(Q(coupon_code__icontains=key))
    else:
        coupon = Coupon.objects.all()

    context = {
        'coupons': coupon
    }

    return render(request, 'admin_panel/coupon_management.html', context)


def update_coupon(request, coupon_id):
    try:
        coupon = Coupon.objects.get(id=coupon_id)

        if request.method == 'POST':
            coupon_code = request.POST['coupon_code'] 
            minimum_amount = request.POST['minimum_amount'] 
            discount_price = request.POST['discount_price'] 
            expiry_at = request.POST['expiry_at'] 

            coupon.coupon_code = coupon_code
            coupon.minimum_amount = minimum_amount
            coupon.discount_price = discount_price
            coupon.expiry_at = expiry_at

            coupon.save()
            return redirect('coupon_management')

        context = {
            'coupon': coupon
        }
    except Exception as e:
        raise e
    
    return render(request, 'admin_panel/update_coupon.html', context)



def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.filter(id=coupon_id)
    coupon.delete()
    return redirect('coupon_management')


def add_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST['coupon_code'] 
        minimum_amount = request.POST['minimum_amount'] 
        discount_price = request.POST['discount_price'] 
        expiry_at = request.POST['expiry_at']

        coupon = Coupon(
            coupon_code=coupon_code,
            minimum_amount=minimum_amount,
            discount_price=discount_price,
            expiry_at=expiry_at
        )

        coupon.save()
        return redirect('coupon_management')
    return render(request, 'admin_panel/add_coupon.html')