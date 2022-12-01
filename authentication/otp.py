from twilio.rest import Client
from authentication.models import Account, VerificationUser
from frost_fad.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SERVICE_SID
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse,HttpResponse



def send_otp(phone_number, user_inst):
    number = '+91' + str(phone_number)
    account_sid = TWILIO_ACCOUNT_SID

    auth_token = TWILIO_AUTH_TOKEN
    service_id = TWILIO_SERVICE_SID
    client = Client(account_sid, auth_token)
    verification  = client.verify \
                    .services(service_id) \
                    .verifications \
                    .create(to=number, channel='sms')
    

    if VerificationUser.objects.filter(user = user_inst).exists():
        user=get_object_or_404(VerificationUser,user=user_inst)
        print(user)
        user.otp_attempt+=1
        user.save()
    else:
        user=VerificationUser()
        user.user=user_inst
        user.otp_attempt+=1
        user.save()
    print(verification.sid)
    return  user.id



def verify_otp(phone_number, otp):
    number = '+91' + str(phone_number)
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    service_id = TWILIO_SERVICE_SID
    client = Client(account_sid, auth_token)
    print('verification checking..........')
    verification_check = client.verify \
                        .services(service_id) \
                        .verification_checks \
                        .create(to=number,  code=otp)
    # print("After verification......................................")
    if verification_check.status=="approved":
        print('verification confirm')
        return True
    else:
        message.error
        return False



def otp_verify_code(request, phone_number, uid, verification_user):
    try:
        if request.method == 'POST':
            otp = request.POST.get('otp')

            verify = verify_otp(phone_number, otp)
            if verify:
                user = Account.object.get(pk=uid)
                user.is_active=True
                user.save()
                user_verif= VerificationUser.objects.get(pk=verification_user)
                user_verif.otp = otp
                user_verif.otp_verification = True
                user_verif.save()
                
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'invalid otp recheck')
                return redirect('activate_email')
        
        return render(request, 'authentication/enterotp.html')

    except:

            return HttpResponse('404 NOT FOUND ERROR')

     
     

def resend_otp(request):
    phone_number=request.GET.get('phone_number', None)
    uid=request.GET.get('uid', None)
    user_inst=get_object_or_404(Account,pk=uid)
    # verification_user=get_object_or_404(VerificationUser,user=user_instence)
    send_otp(phone_number,user_inst)
    data={
        'status': True
    }
    print(data['status'])
    return JsonResponse(data)