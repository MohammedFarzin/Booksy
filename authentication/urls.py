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


    path('forgotpassword/', views.forgot_password, name="forgot_password"),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name="reset_password_validate"),
    path('reset_password/', views.reset_password, name="reset_password"),

    path('order_detail/<int:order_id>/', views.order_detail, name="order_detail"),

    
    #dashboard
    path('dashboard/', views.dashboard, name="dashboard"),
    path('my_orders/', views.my_orders, name="my_orders"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('cancel_order_user/<int:order_number>', views.cancel_order_user, name="cancel_order_user"),

    
    
]