from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import OrderForm
from cart.models import CartItems
from .models import Order, OrderProduct, Payment, Coupon
import datetime
from django.utils import timezone
from django.template.loader import render_to_string

# Razorpay

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse

# product

from store.models import Product

# Create your views here.

# authorize razorpay client with API Keys.


def razorpay_check(request):

    if request.method == "POST":
        payment_order = Payment()
        payment_order.user = request.user
        payment_order.payment_method = request.POST.get('payment_mode')
        if request.POST.get('payment_id'):
            payment_order.payment_id = request.POST.get('payment_id')
        payment_order.amount_paid = request.POST.get('grand_total')
        payment_order.status = True
        payment_order.save()
        print("payment is saved")

        order_number = request.POST.get('order_no')
        order = Order.objects.get(user=request.user, order_number=order_number)
        order.payment = payment_order
        order.is_ordered = True
        order.status = 'Processing'
        order.order_total = request.POST.get('grand_total')
        order.save()

        # moving the order details into order product table

        cart_items = CartItems.objects.filter(user=request.user)
        for cart_item in cart_items:
            order_product = OrderProduct()
            order_product.order = order
            order_product.payment = payment_order
            order_product.user = request.user
            order_product.product = cart_item.product
            order_product.quantity = cart_item.quantity
            order_product.product_price = cart_item.product.price
            order_product.ordered = True
            order_product.save()

            item = CartItems.objects.get(id=cart_item.id)
            product_variation = item.variations.all()
            order_product = OrderProduct.objects.get(id=order_product.id)
            order_product.variation.set(product_variation)
            order_product.save()

            # reducing the quantity of product after selling it
            product = Product.objects.get(id=cart_item.product_id)
            product.stock -= cart_item.quantity
            product.save()

        # deleting the cart itemszzzzzzzzzzzzzzz
        CartItems.objects.filter(user=request.user).delete()

        # send order number and transaction id

        data = {
            'order_number': order_number,
            'tansID': payment_order.payment_id,
        }

        return JsonResponse({'status': 'Your order placed successfully!', 'data': data})

# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.


def order_completed(request):
    order_number = request.GET.get('order_number')
    print(order_number)

    try:
        order = Order.objects.get(order_number=order_number)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        subtotal = 0

        for item in ordered_products:
            subtotal += (item.product_price * item.quantity)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order_number,
            'sub_total': subtotal
        }
        return render(request, 'orders/order_complete.html', context)
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # checking the cart item is exist or not
    cart_items = CartItems.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('product')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price*cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2*total)/100
    grand_total = total+tax

    print('this is try block')

    if request.method == 'POST':
        print('POST')
        form = OrderForm(request.POST)
        if form.is_valid():
            print('form is valid')
            # Store all the billling information inside the order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # generate order_id
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=current_user, is_ordered=False, order_number=order_number)

            # client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            # data = {"amount": int(grand_total) * 100, "currency": "INR", "receipt": "order_rcptid_12"}
            # payment_response = client.order.create(data=data)
            # print(payment_response)

            # order_id = payment_response['id']
            # order_status = payment_response['status']
            # if order_status == 'created':
            #     payment = Payment(
            #         user = current_user,
            #         amount_paid = grand_total,

            #         status = order_status

            #     )
            #     payment.save()

            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'cart_count': cart_count
            }

            return render(request, 'orders/payments.html', context)


def apply_coupon(request):
    coupon_code = request.GET['coupon_code']
    if Coupon.objects.filter(coupon_code__exact=coupon_code, is_active=True).exists():
        coupon = Coupon.objects.filter(coupon_code__exact=coupon_code, is_active=True)
        order_number = request.GET['order_number']
        order = Order.objects.get(order_number=order_number)
        print('ABOVE THE ERROR================================================')
        if not Order.objects.filter(user=request.user, coupon=coupon[0]):
            print('THE COUPON DOESNOT USED================================================================================')
            if coupon.filter(expiry_at__gte=timezone.now()):
                if order.order_total > coupon[0].minimum_amount:
                    print('THIS IS MORETHAN MINIMUM AMOUNT')
                    order.coupon = coupon[0]
                    print(order.coupon)
                    order.coupon_discount = coupon[0].discount_price
                    print(order.coupon_discount)
                    order.order_total -= coupon[0].discount_price
                    print(order.order_total)
                    order.save()
                    messages = "Coupon is Applied"
                    print(messages)
                    current_user = request.user
                    cart_items = CartItems.objects.filter(user=current_user)
                    tax = 0
                    total_amount = 0
                    for cart_item in cart_items:
                        total_amount += (cart_item.product.price *
                                         cart_item.quantity)
                    tax = (2*total_amount)/100
                    sub_total = total_amount-tax
                    coupon_discount = coupon[0].discount_price
                    total_amount -= coupon_discount

                    context = {
                        'order': order,
                        'cart_items': cart_items,
                        'total_amount': total_amount,
                        'tax': tax,
                        'sub_total': sub_total,
                        'coupon_discount': coupon_discount
                    }

                    t = render_to_string('orders/renderpayment.html', context)
                    print(" THIS IS BLELOW THE T")
                    return JsonResponse({'data': t, 'msg': messages})

                else:
                    messages = "You need to purchase minimum amount of " + str(coupon[0].minimum_amount) + " to apply this coupon"
                    return JsonResponse({'msg': messages})
            else:
                messages = "Coupon is Expired"
                return JsonResponse({'msg': messages})
        else:
            print('THE COUPON IS ALREADY IS USED')
            messages = "Coupon is Already is used"
            return JsonResponse({'msg': messages})
    else:
        messages = "Coupon is Invalid"
        return JsonResponse({'msg': messages})
