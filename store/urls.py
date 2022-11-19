from django.urls import path
from . import views


urlpatterns = [
    path('', views.product, name='product'),
    path('category/<slug:category_slug>/', views.product, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_details'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_details'),
    path('author/<slug:author_slug>/', views.author_details, name='author_details'),
    path('search/', views.search, name='search'),

    #Rating and review
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]