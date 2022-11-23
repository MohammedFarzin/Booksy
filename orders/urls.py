from django.urls import path
from . import views


urlpatterns = [
    
    path('place_order/', views.place_order, name='place_order'),
    path('proceed-to-pay/', views.razorpay_check, name='razorpay_check'),
    path('order-completed', views.order_completed, name="order_completed"),
    # path('paymenthandler/', views.paymenthandler, name='paymenthandler'),

]