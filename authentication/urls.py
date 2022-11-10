from django.urls import path

from authentication import otp

from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout', views.signout,name='signout'),
    path('otp-verify/<int:phone_number>/<int:uid>/<int:verification_user>',otp.otp_verify_code,name='otp_verify_code'),
    path('resend-otp',otp.resend_otp,name='resend_otp'),
    path('activate_email/<uidb64>/<token>', views.activate_email, name='activate_email'),
    path('signin/phone_number_page', views.phone_number_page, name='phone_number_page'),
    
]