from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.adminpanel, name="adminpanel"),
    path('user_management/', views.user_management, name="user_management"),
    path('category_management/', views.category_management, name="category_management"),
    path('add_category/', views.add_category, name='add_category'),
    path('order_management/', views.order_management, name="order_management"),
    path('product_management/', views.product_management, name="product_management"),
    path('author_management/', views.author_management, name="author_management"),
    path('variation_management/', views.variation_management, name="variation_management"),
    path('admin_orders/', views.admin_order, name="admin_orders"),
    path('review_management/', views.review_management, name="review_management"),
    path('admin_change_password/', views.admin_change_password, name='admin_change_password'),
    path('coupon_management/', views.coupon_management, name="coupon_management"),
    

    
    # user management

    path('user_ban/<int:user_id>/',views.user_ban,name='user_ban'),
    path('user_unban/<int:user_id>/',views.user_unban,name='user_unban'),

    # category management

    path('update_category/<int:category_id>/', views.update_category, name="update_category"),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),

    # Product management

    path('add_product/',views.add_product,name='add_product'),
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),

    # Variation management

    path('add_variation/', views.add_variation, name='add_variation'),
    path('update_variation/<int:variation_id>/',views.update_variation,name='update_variation'),
    path('delete_variation/<int:variation_id>/', views.delete_variation, name='delete_variation'),
    

    # Author management

    path('add_author/', views.add_author, name='add_author'),
    path('update_author/<int:author_id>/',views.update_author,name='update_author'),
    path('delete_author/<int:author_id>/', views.delete_author, name='delete_author'),

    # Order management
    path('manager_cancel_order/<int:order_number>/', views.manager_cancel_order, name='manager_cancel_order'),
    path('accept_order/<int:order_number>/', views.accept_order, name='accept_order'),
    path('complete_order/<int:order_number>/', views.complete_order, name='complete_order'),
    path('cancel_order/<int:order_number>/', views.cancel_order, name='cancel_order'),

    #review_management

    path('review_block/<int:review_id>/', views.review_block, name="review_block"),
    path('review_unblock/<int:review_id>/', views.review_unblock, name="review_unblock"),

    #coupon_management
    path('add_coupon', views.add_coupon, name="add_coupon"),
    path('update_coupon/<int:coupon_id>/', views.update_coupon, name="update_coupon"),
    path('delete_coupon/<int:coupon_id>/', views.delete_coupon, name="delete_coupon"),

]