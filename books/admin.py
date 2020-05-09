from django.contrib import admin

from .models import Ebook, Autor, Gendre, Publisher, Format, Banner, MainBanner

admin.site.register(Ebook)
admin.site.register(Autor)
admin.site.register(Gendre)
admin.site.register(Publisher)
admin.site.register(Format)
admin.site.register(Banner)
admin.site.register(MainBanner)