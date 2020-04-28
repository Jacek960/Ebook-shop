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
        discount = self.price_brutto * self.discount_percent
        price_discount_added = self.price_brutto - discount
        return price_discount_added

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
