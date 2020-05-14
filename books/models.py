from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Autor(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name.lower().replace('ł', 'l'))
        super(Autor, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Gendre(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name.lower().replace('ł', 'l'))
        super(Gendre, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Format(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


VAT_TYPS = (
    (0, "0 %"),
    (1, "5 %"),
    (2, "8 %"),
    (3, "23 %")
)


class Ebook(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=300, blank=True, null=True)
    description = models.TextField()
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    gendre = models.ManyToManyField(Gendre)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    vat = models.IntegerField(choices=VAT_TYPS)
    discount_percent = models.IntegerField(default=0, validators=
    [MinValueValidator(0),
     MaxValueValidator(100)])
    format = models.ManyToManyField(Format)
    image = models.ImageField(upload_to='ad_image/', blank=True, null=True)
    file_upload_1 = models.FileField(upload_to='uploads/')
    file_upload_2 = models.FileField(upload_to='uploads/')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug  and self.name and self.autor:
            self.slug = slugify(f"{self.name.lower().replace('ł', 'l')}-{self.autor.slug}")
        super(Ebook, self).save(*args, **kwargs)

    def price_brutto(self):
        if self.vat == 0:
            return self.price
        elif self.vat == 1:
            return float(self.price) * 1.05
        elif self.vat == 2:
            return float(self.price) * 1.08
        elif self.vat == 3:
            return float(self.price) * 1.23

    def price_brutto_discount(self):
        discount = float(self.price) * (float(self.discount_percent)/100)
        price_discount_added = float(self.price) - float(discount)
        if self.vat == 0:
            return price_discount_added
        elif self.vat == 1:
            return price_discount_added * 1.05
        elif self.vat == 2:
            return price_discount_added * 1.08
        elif self.vat == 3:
            return price_discount_added * 1.23



    def vat_string(self):
        if self.vat == 0:
            return '0 %'
        elif self.vat == 1:
            return "5 %"
        elif self.vat == 2:
            return '8 %'
        elif self.vat == 3:
            return '23 %'

    def __str__(self):
        return self.name

class Banner(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='books/static/img/baner/')
    url = models.CharField(max_length=350)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class MainBanner(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='books/static/img/baner/')
    url = models.CharField(max_length=350)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    product = models.ManyToManyField(Ebook,through='CartProduct')

    def __str__(self):
        return self.user.username

class CartProduct(models.Model):
    product = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)



    def __str__(self):
        return self.product.name
