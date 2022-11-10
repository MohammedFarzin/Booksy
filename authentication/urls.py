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

    #dashboard
    path('dashboard/', views.dashboard, name="dashboard"),

    path('forgotpassword/', views.forgot_password, name="forgot_password"),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name="reset_password_validate"),
    path('reset_password/', views.reset_password, name="reset_password"),

    
    
]