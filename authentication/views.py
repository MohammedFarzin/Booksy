from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from authentication.forms import RegistrationForm
from .models import *
from .otp import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                first_name=form.cleaned_data['first_name']
                last_name=form.cleaned_data['last_name']
                email=form.cleaned_data['email']
                phone_number=form.cleaned_data['phone_number']
                password=form.cleaned_data['password']
                

                user = Account.object.create_user(first_name = first_name, last_name = last_name, email = email, phone_number = phone_number, password = password )
                user.save()

                #USER ACTIVATION
                # verification_user = send_otp(phone_number, user)
                current_site = get_current_site(request)
                mail_subject = 'Please activate your account'
                message = render_to_string('authentication/account_verification_email.html', {
                    'user': user,
                    'domain' : current_site,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                    'token' : default_token_generator.make_token(user),
                    # 'phone_number' : phone_number,
                    # 'uid' : user.pk,
                    # 'verification_user' : verification_user,
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                messages.success(request, 'Thank you for registering, We have send you an verification email ,please check the email and enter the otp to verify')




                # messages.success(request, 'Thank you for registering, We have send you an verification email ,please cheack the email to verify') 
                return redirect('signup')
                

                # verification_user = send_otp(phone_number, user)
                # return redirect('otp_verify_code', phone_number=phone_number,uid=user.pk,verification_user=verification_user)


            else:
                messages.warning(request, 'Form not submitted try again....')
                return redirect('signup')
        else:
            form = RegistrationForm()
    return render(request, 'authentication/signup.html', {'form' : form})




def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email,password=password)
                
            if user is not None:
                login(request,user)
                return redirect('home')
            else :
                messages.error(request,'Incorrect Username or Password')
                return redirect('signin') 
                    
        
    return render(request,'authentication/signin.html')



@login_required(login_url = 'signin')
def signout(request):
        print("this is log")

        logout(request)
        print("this is logout")
        messages.success(request, 'Logout successful')
        return redirect('signin')       



    


def activate_email(request, uidb64, token):
    try:
        uid =urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations you are activated your account")
        return redirect('signin')
    else:
        messages.error(request, 'You are not activated your account')
        return redirect('signup')


def phone_number_page(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if Account.object.filter(phone_number=phone_number).exists():
            user = Account.object.get(phone_number__exact = phone_number)
            verification_user = send_otp(phone_number, user)
            context = {
                'phone_number' : phone_number,
                'uid' : user.pk,
                'verification_user' : verification_user,
            }
            messages.success(request, 'OTP send to your phone number')
            return render(request, 'authentication/enterotp.html', context)
        else:
            messages.error(request, 'Invalid phone number')
            return redirect('phone_number_page')    
    return render(request, 'authentication/phone_number_page.html' )




@login_required(login_url = 'signin')
def dashboard(request):
    return render(request, 'authentication/dashboard.html')



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
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                # 'phone_number' : phone_number,
                # 'uid' : user.pk,
                # 'verification_user' : verification_user,
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Passwrod reset email had been send to your email')
            return redirect('signin')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')

    return render(request, 'authentication/forgot_password.html')




def reset_password_validate(request, uidb64, token):
    try:
        uid =urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
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

