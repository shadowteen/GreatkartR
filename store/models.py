from django.db import models
from category.models import Category , SubCategory
from django.urls import reverse
from tinymce.models import HTMLField

# Create your models here.

class Product(models.Model):
    skuno = models.CharField(max_length=200, unique=True)
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = HTMLField()
    brand = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    width = models.CharField(max_length=10, blank=True)
    height = models.CharField(max_length=10, blank=True)
    diameter = models.CharField(max_length=10, blank=True)
    terrain = models.CharField(max_length=20, blank=True)


    ah = models.CharField(max_length=20, blank=True)
    cca = models.CharField(max_length=20, blank=True)

    price = models.IntegerField()
    discount = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')

    subimgs = models.ImageField(upload_to='photos/products',blank=True, null=True,)
    brandimg = models.ImageField(upload_to='photos/products', blank=True, null=True,)
    

    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) 
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.brand, self.slug])

    def get_selling(self):
        return int(self.price * ((100-self.discount)/100))

    def __str__(self):
        return self.product_name


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="store/products", max_length=255)

    def __str__(self):
        return self.product.product_name