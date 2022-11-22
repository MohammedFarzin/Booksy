from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, UserProfileForm, UserForm
from .models import *
from .otp import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# cart
from cart.views import _cart_id
from cart.models import Cart, CartItems

#Order

from orders.models import OrderProduct, Order
# requests
import requests

# dashboard
from orders.models import Order


# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']

                user = Account.object.create_user(
                    first_name=first_name, last_name=last_name, email=email, phone_number=phone_number, password=password)
                user.save()

                # USER ACTIVATION
                # verification_user = send_otp(phone_number, user)
                current_site = get_current_site(request)
                mail_subject = 'Please activate your account'
                message = render_to_string('authentication/account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    # 'phone_number' : phone_number,
                    # 'uid' : user.pk,
                    # 'verification_user' : verification_user,
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(
                    request, 'Thank you for registering, We have send you an verification email ,please check the email and enter the otp to verify')

                # messages.success(request, 'Thank you for registering, We have send you an verification email ,please cheack the email to verify')
                return redirect('signup')

                # verification_user = send_otp(phone_number, user)
                # return redirect('otp_verify_code', phone_number=phone_number,uid=user.pk,verification_user=verification_user)

            else:
                messages.warning(request, 'Form not submitted try again....')
                return redirect('signup')
        else:
            form = RegistrationForm()
    return render(request, 'authentication/signup.html', {'form': form})


def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exist = CartItems.objects.filter(
                        cart=cart).exists()

                    if is_cart_item_exist:
                        cart_item = CartItems.objects.filter(cart=cart)

                        # Getting the product variations by cart id
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        # Get the cart items from the user to access their product variations
                        cart_item = CartItems.objects.filter(user=user)
                        exist_var_list = []
                        id = []

                        for item in cart_item:
                            exisitng_variation = item.variations.all()
                            exist_var_list.append(list(exisitng_variation))
                            id.append(item.id)

                        for pr in product_variation:
                            if pr in exist_var_list:
                                index = exist_var_list.index(pr)
                                item_id = id[index]
                                item = CartItems.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItems.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                except:
                    pass

                login(request, user)
                # messages.success(request, 'Logged in successfully')
                # here we get the http://127.0.0.1:8000/authentication/signin/?next=/cart/checkout/ url
                url = request.META.get('HTTP_REFERER')
                print(url)

                try:
                    # here we get the next=/cart/checkout/ url
                    query = requests.utils.urlparse(url).query
                    print(query)
                    # Now from here we gonna split it
                    params = dict(x.split('=') for x in query.split('&'))
                    print('params -------------->> ', params)
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:
                    return redirect('home')

            else:
                messages.error(request, 'Incorrect Username or Password')
                return redirect('signin')

    return render(request, 'authentication/signin.html')


@login_required(login_url='signin')
def signout(request):
    print("this is log")

    logout(request)
    print("this is logout")
    messages.success(request, 'Logout successful')
    return redirect('signin')


def activate_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Congratulations you are activated your account")
        return redirect('signin')
    else:
        messages.error(request, 'You are not activated your account')
        return redirect('signup')


def phone_number_page(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if Account.object.filter(phone_number=phone_number).exists():
            user = Account.object.get(phone_number__exact=phone_number)
            verification_user = send_otp(phone_number, user)
            context = {
                'phone_number': phone_number,
                'uid': user.pk,
                'verification_user': verification_user,
            }
            messages.success(request, 'OTP send to your phone number')
            return render(request, 'authentication/enterotp.html', context)
        else:
            messages.error(request, 'Invalid phone number')
            return redirect('phone_number_page')
    return render(request, 'authentication/phone_number_page.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.object.filter(email=email).exists():
            user = Account.object.get(email__exact=email)
            print(user)
            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('authentication/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                # 'phone_number' : phone_number,
                # 'uid' : user.pk,
                # 'verification_user' : verification_user,
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(
                request, 'Passwrod reset email had been send to your email')
            return redirect('signin')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')

    return render(request, 'authentication/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('signin')


def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.object.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('signin')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    else:
        return render(request, 'authentication/reset_password.html')

    

# DASHBOARD

@login_required(login_url='signin')
def dashboard(request):
    orders = Order.objects.order_by(
        '-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile' : userprofile
    }
    return render(request, 'authentication/dashboard.html', context)


def my_orders(request):
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'authentication/my_orders.html', context)


def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=user_profile)
    context = {
        'user_form': user_form,
        'profile_form': user_profile_form,
        'userprofile': user_profile
    }

    return render(request, 'authentication/edit_profile.html', context)



def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.object.get(email__exact=request.user.email)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully')
                return redirect('change_password') 
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')

        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
        
    return render(request, 'authentication/change_password.html')



def order_detail(request, order_number):
    order_detail = OrderProduct.objects.filter(order__order_number=order_number)
    order = Order.objects.get(order_number=order_number)

    subtotal = 0

    for i in order_detail:
        subtotal += (i.product_price * i.quantity) - order.tax
    context = {
        'order_detail': order_detail,
        'order' : order,
        'subtotal' : subtotal
    }
    return render(request, 'authentication/order_detail.html',  context)




def cancel_order_user(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        order.status = 'Cancelled'
        order.save()

        return redirect('my_orders')
        
    except Exception as e:
        raise e

