from django.db import models
from autoslug import AutoSlugField
import os
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique = True)
    slug = AutoSlugField(populate_from = 'category_name' , unique = True, default = None)
    description = models.TextField(max_length=500, blank = True)
    cat_image = models.ImageField(upload_to = 'photos/categories/' , blank = True)
    # created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])



    def __str__(self):
        return self.category_name