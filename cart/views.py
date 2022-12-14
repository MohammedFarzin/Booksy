from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product, Variation
from .models import Cart,CartItems
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from authentication.models import UserProfile



# Create your views here.

#cart
def cart(request, total=0, quantity=0, cart_items=None):
    
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items = CartItems.objects.filter(user=request.user)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItems.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request, 'cart/cart.html', context)



def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart



def add_cart(request, product_id):
    current_user = request.user
    product=Product.objects.get(id=product_id)#get product

    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                print(key, value)
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_values__iexact=value)
                    product_variation.append(variation)               
                except:
                    pass

        

        is_cart_item_exists =  CartItems.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item=CartItems.objects.filter(product=product, user=current_user)
            exist_var_list = []  #existing_variations from database
            id = []
            for item in cart_item:
                exisiting_variation = item.variations.all()
                print(exisiting_variation)
                exist_var_list.append(list(exisiting_variation))
                id.append(item.id)
            
            print(exist_var_list)
            if product_variation in exist_var_list:
                #increase item quantity in cart
                index = exist_var_list.index(product_variation)
                item_id = id[index]
                item = CartItems.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create a new cart item
                item = CartItems.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item=CartItems.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    else:
        product_variation = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST.get(key)
                print(key, value)
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_values__iexact=value)
                    product_variation.append(variation)               
                except:
                    pass

        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))#get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists =  CartItems.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item=CartItems.objects.filter(product=product, cart=cart)
            exist_var_list = []  #existing_variations from database
            id = []
            for item in cart_item:
                exisiting_variation = item.variations.all()
                print(exisiting_variation)
                exist_var_list.append(list(exisiting_variation))
                id.append(item.id)
            
            print(exist_var_list)
            if product_variation in exist_var_list:
                #increase item quantity in cart
                index = exist_var_list.index(product_variation)
                item_id = id[index]
                item = CartItems.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create a new cart item
                item = CartItems.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item=CartItems.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')



def remove_cart(request, product_id, cart_item_id):
    product=get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItems.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItems.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')



def remove_cart_item(request, product_id, cart_item_id):
    product=get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItems.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItems.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
        return redirect('cart')
    except:
        pass


@login_required(login_url='signin')
def checkout(request, total=0, quantity=0, cart_items=None):
    
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItems.objects.filter(user=request.user)

            userprofile = UserProfile.objects.filter(user=request.user).first()
            print(userprofile) 
        
        for cart_item in cart_items:
            total += (cart_item.product.price*cart_item.quantity)
            quantity += cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        'userprofile': userprofile,
    }
    return render(request, 'cart/checkout.html', context)








    