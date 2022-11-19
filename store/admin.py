from django.contrib import admin
from .models import Product,Variation,ReviewRating,Author
# Register your models here.
from django.contrib import admin


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name' , 'price', 'stock', 'category', 'created_date', 'modified_date', 'is_available')


class VariationModels(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_values', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_values')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationModels)
admin.site.register(ReviewRating)
admin.site.register(Author)