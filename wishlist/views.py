from django.shortcuts import render, redirect, get_object_or_404
from .models import WishlistItems, Wishlist
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from wishlist.models import Variation
from django.http import JsonResponse


# Create your views here.




def wishlist(request):
    try:
        if request.user.is_authenticated:
            wishlist_items = WishlistItems.objects.filter(user=request.user)
        else:
            return redirect('signin')
    except ObjectDoesNotExist:
        pass

    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist/wishlist.html', context)


def add_wishlist(request):
    
            
        if request.method == "GET":
            prod_id = request.GET['prod_id']
            current_user = request.user
            product = Product.objects.get(id=prod_id)
            print('go tproduct')  # get product

            if current_user.is_authenticated:
                print('user authenticated')

                # is_wishlist_item_exists = WishlistItems.objects.filter(
                #     product=product, user=current_user).exists()
                # if is_wishlist_item_exists:
                #     return redirect('wishlist')

                # else:
                wishlist_item = WishlistItems.objects.create(
                        product=product,
                        user=current_user,
                    )

                wishlist_item.save()
                data = {
                    'message' : 'Wishlist added successfully',
                }

                print('json JsonResponse')
                return JsonResponse(data)
            else:
                data = {
                        'message':'Please login',
                    }
                return JsonResponse(data)

    


def remove_wishlist(request):
    if request.user.is_authenticated:

        print('remove wish list')
        if request.method == 'GET':
            prod_id = request.GET['prod_id']
            product = Product.objects.get(id=prod_id)
            print(product)
            try:
                print('hai')
                if request.user.is_authenticated:                
                    wishlist_item = WishlistItems.objects.get(product=product, user=request.user)
                
                    wishlist_item.delete()
                    data = {
                        'message':'Wishlist removed successfully',
                    }
                    return JsonResponse(data)
                else:
                    data = {
                        'message':'Please login',
                    }
                    return JsonResponse(data)
            except:
                print('EXCEPT BLOCK')


def remove_wishlist_item(request, product_id, wishlist_item_id):
    product=get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            wishlist_item=WishlistItems.objects.get(product=product, user=request.user, id=wishlist_item_id)
        
        wishlist_item.delete()
        return redirect('wishlist')
    except:
        pass